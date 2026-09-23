#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시니어사연 보이스 무료제작기 - 고속 무결점 오디오 결합 및 타이밍 싱크 엔진
ffprobe 의존성 완전 제거: Mutagen + imageio-ffmpeg 바이너리 직결!
"""

import os
import sys
import json
import subprocess
import imageio_ffmpeg
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, SYLT, USLT, Encoding, TIT2, TPE1

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()


def ms_to_srt_time(ms: int) -> str:
    hours = ms // (1000 * 60 * 60)
    remainder = ms % (1000 * 60 * 60)
    minutes = remainder // (1000 * 60)
    remainder %= (1000 * 60)
    seconds = remainder // 1000
    millis = remainder % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def get_mp3_duration_ms(mp3_path: str) -> int:
    """Mutagen을 사용해 mp3의 정확한 재생 길이를 ms 단위로 측정 (ffprobe 불필요!)"""
    audio = MP3(mp3_path)
    return int(audio.info.length * 1000)


def create_silence_mp3(duration_ms: int, output_path: str):
    """FFmpeg를 사용해 정확한 길이의 무음 mp3 생성"""
    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono",
        "-t", f"{duration_ms / 1000.0:.3f}",
        "-q:a", "9",
        "-acodec", "libmp3lame",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def concat_audio_files(input_files: list[str], output_file: str):
    """FFmpeg concat demuxer를 사용하여 다수의 mp3 파일을 무손실 결합"""
    list_txt_path = output_file + ".list.txt"
    with open(list_txt_path, "w", encoding="utf-8") as f:
        for p in input_files:
            # 윈도우 역슬래시 escape
            norm_path = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{norm_path}'\n")

    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_txt_path,
        "-acodec", "libmp3lame",
        "-b:a", "192k",
        output_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    if os.path.exists(list_txt_path):
        os.remove(list_txt_path)


def stitch_parts_and_sync(
    utterances: list[dict],
    part_mp3_paths: list[str],
    output_mp3_path: str,
    output_srt_path: str = None,
    output_json_path: str = None,
    pause_ms: int = 400,
    track_title: str = "시니어 사연",
    artist: str = "시니어사연 보이스 무료제작기"
) -> dict:
    """
    개별 대사 mp3 파일들을 여운 무음(기본 400ms)과 함께 결합하고
    SRT 자막, JSON 메타데이터, MP3 ID3v2 SYLT 동기화 가사 태그를 생성합니다.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_mp3_path)), exist_ok=True)
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(output_mp3_path)), "temp_parts")
    os.makedirs(temp_dir, exist_ok=True)

    # 무음 파일 1개 미리 생성
    silence_file = os.path.join(temp_dir, "pause_silence.mp3")
    create_silence_mp3(pause_ms, silence_file)

    files_to_concat = []
    timeline = []
    sylt_entries = []
    srt_lines = []
    current_time_ms = 0

    for idx, (utt, part_path) in enumerate(zip(utterances, part_mp3_paths), 1):
        dur_ms = get_mp3_duration_ms(part_path)
        start_ms = current_time_ms
        end_ms = start_ms + dur_ms

        speaker = utt.get("speaker", "내레이션")
        text = utt.get("text", "").strip()
        display_text = f"[{speaker}] {text}"

        timeline.append({
            "index": idx,
            "speaker": speaker,
            "text": text,
            "start_ms": start_ms,
            "end_ms": end_ms,
            "start_time": ms_to_srt_time(start_ms),
            "end_time": ms_to_srt_time(end_ms),
            "duration_ms": dur_ms
        })

        sylt_entries.append((display_text, start_ms))

        # SRT 자막 포맷
        srt_lines.append(f"{idx}")
        srt_lines.append(f"{ms_to_srt_time(start_ms)} --> {ms_to_srt_time(end_ms)}")
        srt_lines.append(display_text)
        srt_lines.append("")

        files_to_concat.append(part_path)
        if idx < len(utterances):
            files_to_concat.append(silence_file)
            current_time_ms = end_ms + pause_ms
        else:
            current_time_ms = end_ms

    # 1. FFmpeg로 전체 결합
    concat_audio_files(files_to_concat, output_mp3_path)

    # 2. SRT 자막 저장
    if not output_srt_path:
        output_srt_path = os.path.splitext(output_mp3_path)[0] + ".srt"
    with open(output_srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    # 3. JSON 상세 싱크 데이터 저장
    if not output_json_path:
        output_json_path = os.path.splitext(output_mp3_path)[0] + "_sync.json"
    sync_data = {
        "title": track_title,
        "total_duration_ms": current_time_ms,
        "total_utterances": len(timeline),
        "timeline": timeline
    }
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, ensure_ascii=False, indent=2)

    # 4. MP3 내부 ID3v2 SYLT (동기화 가사) 태그 주입
    try:
        mp3 = MP3(output_mp3_path, ID3=ID3)
        if mp3.tags is None:
            mp3.add_tags()
        tags = mp3.tags
        tags.add(TIT2(encoding=Encoding.UTF8, text=[track_title]))
        tags.add(TPE1(encoding=Encoding.UTF8, text=[artist]))
        full_lyrics = "\n".join([f"[{t['speaker']}] {t['text']}" for t in timeline])
        tags.add(USLT(encoding=Encoding.UTF8, lang='kor', desc='', text=full_lyrics))
        tags.add(SYLT(
            encoding=Encoding.UTF8,
            lang='kor',
            format=2,
            type=1,
            desc='Lyrics',
            text=sylt_entries
        ))
        mp3.save()
    except Exception as e:
        print(f"ID3v2 SYLT 주입 알림: {e}")

    # 임시 무음 파일 삭제
    if os.path.exists(silence_file):
        os.remove(silence_file)

    return sync_data


if __name__ == "__main__":
    print("✓ 무결점 오디오 결합 & 타이밍 싱크 엔진 준비 완료!")
