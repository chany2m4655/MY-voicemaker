#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Gemini 2.5 Flash 프리미엄 TTS 엔진
Gacrux(가크룩스) 중후한 남성 내레이션 등 고품질 한국어 오디오 생성
"""

import os
import io
import json
import base64
import subprocess
import requests
import imageio_ffmpeg
from dotenv import load_dotenv

load_dotenv()

def get_gemini_api_key():
    return os.getenv("GEMINI_API_KEY")

def generate_gemini_tts(
    text: str,
    voice_name: str = "Gacrux",
    style_instruction: str = "당신은 감동적인 인생사연을 전문적으로 낭독하는 시니어 유튜브 전문 나레이터입니다. 차분하고 중후하며 마음을 울리는 깊은 어조로 천천히 읽어주세요.",
    output_path: str = None
) -> bytes:
    """
    Gemini 2.5 Flash TTS를 호출하여 MP3 바이너리를 반환하거나 output_path에 저장
    """
    api_key = get_gemini_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY가 설정되어 있지 않습니다.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={api_key}"
    
    prompt = f"{style_instruction}\n\n\"{text}\""
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice_name
                    }
                }
            }
        }
    }

    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
    if res.status_code != 200:
        raise RuntimeError(f"Gemini API 오류 ({res.status_code}): {res.text}")

    data = res.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError(f"Gemini API 응답에 candidate가 없습니다: {data}")

    parts = candidates[0].get("content", {}).get("parts", [])
    raw_pcm = None
    for p in parts:
        if "inlineData" in p:
            b64 = p["inlineData"].get("data", "")
            raw_pcm = base64.b64decode(b64)
            break

    if not raw_pcm:
        raise RuntimeError("Gemini API에서 오디오 데이터를 수신하지 못했습니다.")

    # 24kHz 16-bit PCM -> MP3 변환 (FFmpeg stdin/stdout 파이프)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "s16le",
        "-ar", "24000",
        "-ac", "1",
        "-i", "pipe:0",
        "-b:a", "192k",
        "-f", "mp3",
        "pipe:1"
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    mp3_bytes, stderr = proc.communicate(input=raw_pcm)

    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg MP3 인코딩 실패: {stderr.decode('utf-8', errors='ignore')}")

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(mp3_bytes)

    return mp3_bytes
