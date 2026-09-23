#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import asyncio

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import generate_single_audio_file
from scripts.audio_syncer import stitch_parts_and_sync

async def test_section_0():
    print("▶ 섹션 0번 ('발로 찬 남편, 성묘의 추락') 고속 렌더링 테스트 시작...")
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "parsed_story.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sec0 = data["sections"][0]
    print(f"✓ 섹션 제목: {sec0['section_title']}")
    print(f"✓ 총 대사 수: {len(sec0['utterances'])}개")

    sec_dir = os.path.join(os.path.dirname(__file__), "..", "output", "section_00")
    parts_dir = os.path.join(sec_dir, "parts")
    os.makedirs(parts_dir, exist_ok=True)

    part_files = []
    for idx, utt in enumerate(sec0["utterances"], 1):
        speaker = utt["speaker"]
        text = utt["text"]
        part_path = os.path.join(parts_dir, f"part_{idx:03d}.mp3")
        print(f"  [{idx}/{len(sec0['utterances'])}] '{speaker}' 음성 생성 중... ({text[:25]}...)")
        await generate_single_audio_file(speaker, text, part_path)
        part_files.append(part_path)

    mp3_path = os.path.join(sec_dir, "section_00.mp3")
    srt_path = os.path.join(sec_dir, "section_00.srt")
    sync_json_path = os.path.join(sec_dir, "section_00_sync.json")

    print("▶ 오디오 결합 및 SRT 자막, ID3v2 SYLT 동기화 가사 태그 주입 중...")
    result = stitch_parts_and_sync(
        utterances=sec0["utterances"],
        part_mp3_paths=part_files,
        output_mp3_path=mp3_path,
        output_srt_path=srt_path,
        output_json_path=sync_json_path,
        pause_ms=400,
        track_title=sec0["section_title"],
        artist="시니어사연 보이스 무료제작기"
    )

    print("\n" + "="*50)
    print("🎉 섹션 0번 완성 성공!")
    print(f"✓ MP3 파일: {mp3_path} ({os.path.getsize(mp3_path):,} bytes)")
    print(f"✓ SRT 자막: {srt_path}")
    print(f"✓ 총 재생 시간: {result['total_duration_ms'] / 1000:.2f}초")
    print("="*50)

    with open(srt_path, "r", encoding="utf-8") as f:
        print("\n[생성된 SRT 자막 내용]:\n" + f.read())

if __name__ == "__main__":
    asyncio.run(test_section_0())
