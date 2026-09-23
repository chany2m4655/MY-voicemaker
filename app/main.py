#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시니어사연 보이스 무료제작기 - 통합 웹 백엔드 서버 (FastAPI)
"""

import os
import sys
import json
import io
import re
import requests
import asyncio
import imageio_ffmpeg
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydub import AudioSegment

# 로컬 스크립트 모듈 import
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from scripts.drama_parser import parse_script_file, CHARACTER_VOICE_MAP, smart_chunk_text
from scripts.audio_syncer import stitch_parts_and_sync, FFMPEG_EXE
from app.emotion_engine import get_speech_config_and_ssml

app = FastAPI(title="시니어사연 보이스 무료제작기 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 및 출력 경로 설정
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# 전역 프로젝트 상태 저장 객체
STATE = {
    "colab_url": "",
    "is_colab_connected": False,
    "current_project": None,
    "active_voices": dict(CHARACTER_VOICE_MAP),
    "task_status": {}
}


class ColabConnectRequest(BaseModel):
    url: str


class VoiceUpdateRequest(BaseModel):
    speaker_name: str
    speaker_id: str


@app.get("/api/status")
def get_status():
    return {
        "colab_url": STATE["colab_url"],
        "is_colab_connected": STATE["is_colab_connected"],
        "has_project": STATE["current_project"] is not None,
        "title": STATE["current_project"]["title"] if STATE["current_project"] else "프로젝트 없음",
        "total_sections": len(STATE["current_project"]["sections"]) if STATE["current_project"] else 0,
        "task_status": STATE["task_status"]
    }


@app.post("/api/colab/connect")
def connect_colab(req: ColabConnectRequest):
    url = req.url.strip().rstrip("/")
    if not url:
        STATE["colab_url"] = ""
        STATE["is_colab_connected"] = False
        return {"status": "disconnected"}
    
    try:
        res = requests.get(f"{url}/health", timeout=5)
        if res.status_code == 200:
            STATE["colab_url"] = url
            STATE["is_colab_connected"] = True
            return {"status": "connected", "url": url, "data": res.json()}
    except Exception as e:
        STATE["is_colab_connected"] = False
        raise HTTPException(status_code=400, detail=f"코랩 워커 연결 실패: {str(e)}")


from app.voice_bank import VOICE_BANK, get_voice_by_id
from app.gemini_tts import generate_gemini_tts

VOICE_BANK_FILE = os.path.join(DATA_DIR, "voice_bank_custom.json")

def load_voice_bank():
    res = {v["id"]: dict(v) for v in VOICE_BANK}
    if os.path.exists(VOICE_BANK_FILE):
        try:
            with open(VOICE_BANK_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                for item in saved:
                    if item["id"] in res:
                        res[item["id"]].update(item)
                    else:
                        res[item["id"]] = item
        except Exception:
            pass
    return list(res.values())

def save_voice_bank(bank_data):
    with open(VOICE_BANK_FILE, "w", encoding="utf-8") as f:
        json.dump(bank_data, f, ensure_ascii=False, indent=2)

CURRENT_VOICE_BANK = load_voice_bank()


@app.get("/api/voice-bank")
def get_voice_bank_list():
    """22대 전속 성우 목록 반환 (송세아 & 가크룩스 포함)"""
    return {"voice_bank": CURRENT_VOICE_BANK}


@app.get("/api/voice-bank/sample/{voice_id}")
def get_voice_sample(voice_id: str):
    """사전 생성된 성우 샘플 오디오 스트리밍"""
    sample_path = os.path.join(OUTPUT_DIR, "samples", f"{voice_id}.mp3")
    if os.path.exists(sample_path):
        return FileResponse(sample_path, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="샘플 오디오를 찾을 수 없습니다.")


class VoiceTestRequest(BaseModel):
    voice_id: str
    text: str
    rate: str
    pitch: str
    style: str


@app.post("/api/voice-bank/test")
async def test_custom_voice(req: VoiceTestRequest):
    """대표님이 슬라이더로 조절하거나 선택한 성우를 실시간으로 합성해 미리듣기 제공"""
    meta = None
    for v in CURRENT_VOICE_BANK:
        if v["id"] == req.voice_id:
            meta = v
            break
    if not meta:
        meta = CURRENT_VOICE_BANK[0]

    # Gemini 2.5 Flash TTS 엔진 (가크룩스)
    if meta.get("voice") == "gemini-tts-Gacrux" or req.voice_id == "NARRATION_GACRUX":
        try:
            mp3_bytes = generate_gemini_tts(req.text, voice_name="Gacrux")
            return StreamingResponse(io.BytesIO(mp3_bytes), media_type="audio/mpeg")
        except Exception as e:
            print(f"Gemini TTS 합성 실패, edge-tts fallback: {e}")

    # 기본 edge-tts 순수 파라미터 엔진
    import edge_tts
    voice = meta["voice"]
    if voice == "gemini-tts-Gacrux":
        voice = "ko-KR-InJoonNeural"
    comm = edge_tts.Communicate(req.text, voice, rate=req.rate, pitch=req.pitch)
    stream = io.BytesIO()
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            stream.write(chunk["data"])
    stream.seek(0)
    return StreamingResponse(stream, media_type="audio/mpeg")


class VoiceSaveRequest(BaseModel):
    voice_id: str
    rate: str
    pitch: str
    style: str


class VoiceSaveRequest(BaseModel):
    voice_id: str
    rate: str
    pitch: str
    style: str


@app.post("/api/voice-bank/save")
def save_voice_settings(req: VoiceSaveRequest):
    """대표님이 확정한 성우 설정을 영구 저장"""
    for v in CURRENT_VOICE_BANK:
        if v["id"] == req.voice_id:
            v["rate"] = req.rate
            v["pitch"] = req.pitch
            v["style"] = req.style
            break
    save_voice_bank(CURRENT_VOICE_BANK)
    return {"status": "saved", "voice_id": req.voice_id}


class CharacterAssignRequest(BaseModel):
    character_name: str
    voice_id: str


@app.post("/api/characters/assign")
def assign_character_voice(req: CharacterAssignRequest):
    """대본 등장인물에 특정 성우를 매핑"""
    voice_meta = None
    for v in CURRENT_VOICE_BANK:
        if v["id"] == req.voice_id:
            voice_meta = v
            break
    if not voice_meta:
        raise HTTPException(status_code=404, detail="성우를 찾을 수 없습니다.")

    STATE["active_voices"][req.character_name] = {
        "speaker_id": voice_meta["id"],
        "gender": voice_meta["gender"],
        "age_group": voice_meta["age_group"],
        "character_name": f"{req.character_name} ({voice_meta['name']})",
        "style_prompt": voice_meta["desc"],
        "reference_preset": voice_meta["name"],
        "voice": voice_meta["voice"],
        "style": voice_meta["style"],
        "rate": voice_meta["rate"],
        "pitch": voice_meta["pitch"],
        "volume": voice_meta["volume"]
    }
    return {"status": "assigned", "character": req.character_name, "voice": voice_meta["name"]}


@app.get("/api/project")
def get_project():
    if not STATE["current_project"]:
        parsed_path = os.path.join(DATA_DIR, "parsed_story.json")
        if os.path.exists(parsed_path):
            with open(parsed_path, "r", encoding="utf-8") as f:
                STATE["current_project"] = json.load(f)
                
    if not STATE["current_project"]:
        return {"has_project": False}
        
    return {
        "has_project": True,
        "project": STATE["current_project"],
        "active_voices": STATE["active_voices"],
        "voice_bank": CURRENT_VOICE_BANK
    }


@app.post("/api/upload")
async def upload_files(
    script_file: UploadFile = File(...),
    synopsis_file: Optional[UploadFile] = File(None)
):
    """인트로 화면에서 시놉시스와 전체 대본 txt 파일을 멀티 업로드 받아 파싱 및 인물 매칭"""
    script_content = (await script_file.read()).decode("utf-8", errors="replace")
    
    synopsis_data = {}
    if synopsis_file:
        synopsis_content = (await synopsis_file.read()).decode("utf-8", errors="replace")
        try:
            json_match = re.search(r"\{[\s\S]*\"characters\"[\s\S]*\}", synopsis_content)
            if json_match:
                synopsis_data = json.loads(json_match.group(0))
        except Exception:
            pass

    temp_script_path = os.path.join(DATA_DIR, "current_script.txt")
    with open(temp_script_path, "w", encoding="utf-8") as f:
        f.write(script_content)

    parsed = parse_script_file(temp_script_path)
    if synopsis_data and "characters" in synopsis_data:
        parsed["synopsis_characters"] = synopsis_data["characters"]

    parsed_path = os.path.join(DATA_DIR, "parsed_story.json")
    with open(parsed_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)

    STATE["current_project"] = parsed
    return {
        "status": "success",
        "title": parsed["title"],
        "total_sections": parsed["total_sections"],
        "project": parsed
    }


async def generate_single_audio_file(speaker: str, text: str, output_path: str):
    """대사 한 개를 인물별 감정 SSML 및 송세아 내레이션 톤으로 직접 저장"""
    voice_info = STATE["active_voices"].get(speaker, STATE["active_voices"]["내레이션"])
    speaker_id = voice_info.get("speaker_id", "NARRATION")
    
    # 문맥 및 화자 기반 감정 SSML 파라미터 획득
    emotion_cfg = get_speech_config_and_ssml(speaker, text)
    
    # 1. 코랩 워커 우선 사용 (연결된 경우)
    if STATE["is_colab_connected"] and STATE["colab_url"]:
        try:
            colab_api = f"{STATE['colab_url']}/generate"
            payload = {
                "speaker_id": speaker_id,
                "text": text,
                "rate_override": emotion_cfg["rate"],
                "pitch_override": emotion_cfg["pitch"]
            }
            resp = requests.post(colab_api, json=payload, timeout=30)
            if resp.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                return output_path
        except Exception as e:
            print(f"Colab 생성 실패, 로컬 감정 모드 전환: {e}")

    # 2. Gemini 2.5 Flash TTS 모드 (가크룩스 내레이션)
    if speaker_id == "NARRATION_GACRUX" or voice_info.get("voice") == "gemini-tts-Gacrux":
        try:
            generate_gemini_tts(text, voice_name="Gacrux", output_path=output_path)
            return output_path
        except Exception as e:
            print(f"Gemini TTS 합성 실패, edge-tts fallback: {e}")

    # 3. 로컬 무료 모드 (edge-tts 순수 파라미터 직접 저장)
    import edge_tts
    voice = emotion_cfg["voice"]
    if voice == "gemini-tts-Gacrux":
        voice = "ko-KR-InJoonNeural"
    comm = edge_tts.Communicate(text, voice, rate=emotion_cfg["rate"], pitch=emotion_cfg["pitch"], volume=emotion_cfg["volume"])
    await comm.save(output_path)
    return output_path


@app.post("/api/generate/section/{sec_id}")
async def generate_section(sec_id: int):
    """특정 섹션의 모든 대사를 인물 보이스로 합성 후 결합 및 SRT/ID3 SYLT 생성"""
    if not STATE["current_project"]:
        raise HTTPException(status_code=400, detail="프로젝트가 로드되지 않았습니다.")
        
    sec_data = None
    for s in STATE["current_project"]["sections"]:
        if s["section_id"] == sec_id:
            sec_data = s
            break
            
    if not sec_data:
        raise HTTPException(status_code=404, detail="해당 섹션을 찾을 수 없습니다.")

    sec_key = sec_data["section_key"]
    sec_dir = os.path.join(OUTPUT_DIR, sec_key)
    parts_dir = os.path.join(sec_dir, "parts")
    os.makedirs(parts_dir, exist_ok=True)
    
    mp3_path = os.path.join(sec_dir, f"{sec_key}.mp3")
    srt_path = os.path.join(sec_dir, f"{sec_key}.srt")
    json_path = os.path.join(sec_dir, f"{sec_key}_sync.json")

    utterances = sec_data["utterances"]
    part_files = []
    
    STATE["task_status"][sec_key] = {"status": "generating", "progress": 0, "total": len(utterances)}
    
    for idx, utt in enumerate(utterances):
        speaker = utt.get("speaker", "내레이션")
        text = utt.get("text", "")
        part_path = os.path.join(parts_dir, f"part_{idx:03d}.mp3")
        await generate_single_audio_file(speaker, text, part_path)
        part_files.append(part_path)
        STATE["task_status"][sec_key]["progress"] = idx + 1

    # 오디오 결합 및 타이밍 싱크/가사 태그 주입
    sync_res = stitch_parts_and_sync(
        utterances=utterances,
        part_mp3_paths=part_files,
        output_mp3_path=mp3_path,
        output_srt_path=srt_path,
        output_json_path=json_path,
        pause_ms=400,
        track_title=f"{sec_data['section_title']} ({sec_key})",
        artist="시니어사연 보이스 무료제작기"
    )

    STATE["task_status"][sec_key] = {
        "status": "completed",
        "mp3_url": f"/api/download/{sec_key}/{sec_key}.mp3",
        "srt_url": f"/api/download/{sec_key}/{sec_key}.srt",
        "json_url": f"/api/download/{sec_key}/{sec_key}_sync.json",
        "duration_ms": sync_res["total_duration_ms"]
    }

    return {
        "status": "success",
        "section_id": sec_id,
        "section_key": sec_key,
        "result": STATE["task_status"][sec_key],
        "sync_data": sync_res
    }


@app.get("/api/download/{sec_key}/{filename}")
def download_file(sec_key: str, filename: str):
    file_path = os.path.join(OUTPUT_DIR, sec_key, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")


# 정적 파일 서빙 (프론트엔드 UI)
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    print("🚀 '시니어사연 보이스 무료제작기' 웹서버 시작: http://localhost:8080")
    uvicorn.run(app, host="127.0.0.1", port=8080)
