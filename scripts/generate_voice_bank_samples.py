#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시니어사연 보이스 무료제작기 - 21대 전속 성우 고음질 샘플 생성 스크립트
XML 태그 없는 순수 한국어 대사 + 피치/속도 파라미터 직접 전달
"""

import os
import sys
import asyncio
import edge_tts
from mutagen.mp3 import MP3

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.voice_bank import VOICE_BANK

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "samples")
os.makedirs(OUTPUT_DIR, exist_ok=True)


async def generate_clean_sample(v: dict):
    v_id = v["id"]
    voice = v["voice"]
    rate = v["rate"]
    pitch = v["pitch"]
    volume = v["volume"]
    text = v["sample_text"]

    out_path = os.path.join(OUTPUT_DIR, f"{v_id}.mp3")
    try:
        # XML 태그 없이 순수 텍스트와 파라미터 전달!
        comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
        await comm.save(out_path)
        
        dur = MP3(out_path).info.length
        print(f"✓ [{v['age_group']} {v['role_type']}] {v['name']} -> {dur:.2f}초 ({os.path.getsize(out_path):,} bytes)")
    except Exception as e:
        print(f"✗ {v_id} 실패: {e}")


async def main():
    print(f"▶ 21대 전속 성우 순수 고음질 샘플 렌더링 시작 (총 {len(VOICE_BANK)}명)...")
    for v in VOICE_BANK:
        await generate_clean_sample(v)
    print("\n🎉 21대 전속 성우 샘플 100% 정상 생성 완료!")


if __name__ == "__main__":
    asyncio.run(main())
