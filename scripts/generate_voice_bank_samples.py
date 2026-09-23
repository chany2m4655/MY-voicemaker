#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시니어사연 보이스 무료제작기 - 21대 전속 성우 미리듣기 샘플 일괄 렌더링 스크립트
"""

import os
import sys
import asyncio
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.voice_bank import VOICE_BANK

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "samples")
os.makedirs(OUTPUT_DIR, exist_ok=True)


async def generate_sample(voice_meta: dict):
    v_id = voice_meta["id"]
    voice = voice_meta["voice"]
    style = voice_meta["style"]
    style_degree = voice_meta["style_degree"]
    rate = voice_meta["rate"]
    pitch = voice_meta["pitch"]
    volume = voice_meta["volume"]
    text = voice_meta["sample_text"]

    ssml = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='ko-KR'>
    <voice name='{voice}'>
        <mstts:express-as style='{style}' styledegree='{style_degree}'>
            <prosody pitch='{pitch}' rate='{rate}' volume='{volume}'>
                {text}
            </prosody>
        </mstts:express-as>
    </voice>
</speak>"""

    out_path = os.path.join(OUTPUT_DIR, f"{v_id}.mp3")
    try:
        comm = edge_tts.Communicate(ssml, voice)
        await comm.save(out_path)
        print(f"✓ [{voice_meta['age_group']} {voice_meta['role_type']}] {voice_meta['name']} 샘플 생성 완료")
    except Exception as e:
        print(f"✗ {v_id} 실패: {e}")


async def main():
    print(f"▶ 21대 전속 성우 샘플 렌더링 시작 (총 {len(VOICE_BANK)}명)...")
    for v in VOICE_BANK:
        await generate_sample(v)
    print("🎉 21대 전속 성우 샘플 생성 완료!")


if __name__ == "__main__":
    asyncio.run(main())
