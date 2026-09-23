#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시니어사연 보이스 무료제작기 - 대본 파서 (Drama Parser)
대표님이 주신 시니어 사연 원본 대본을 분석하여:
1. 섹션 0~15 자동 분리
2. [화자] 태그 감지 및 남녀 연령대별 캐릭터 보이스 매핑
3. 문맥 손상 없는 스마트 청킹 (80~120자 단위)
4. JSON 구조화 출력 (data/parsed_story.json)
"""

import json
import os
import re
import sys

# Windows 콘솔 UTF-8 입출력 강제 설정
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 남녀 연령대별 캐릭터 보이스 정의
CHARACTER_VOICE_MAP = {
    # 메인 내레이션: 송세아 (Vrew 시니어 사연 1위 공식 보이스)
    "내레이션": {
        "speaker_id": "NARRATION",
        "gender": "female",
        "age_group": "middle",
        "character_name": "송세아 (메인 내레이터)",
        "style_prompt": "여성 40대 중년, Vrew 1위 송세아 특유의 중후하고 지적이며 편안하고 차분한 심야 라디오 낭독 톤",
        "reference_preset": "song_seah_senior_radio"
    },
    # 주인공 이정희 (여성, 65세 노년)
    "이정희": {
        "speaker_id": "FEMALE_SENIOR_LEAD",
        "gender": "female",
        "age_group": "senior",
        "character_name": "이정희 (주인공, 65세)",
        "style_prompt": "여성 60대 노년, 30년 미용사 출신, 가녀리지만 삶의 연륜과 억눌린 슬픔, 단호하고 온화한 음색",
        "reference_preset": "female_senior_warm"
    },
    # 남편 김병수 (남성, 70세 노년 악역)
    "김병수": {
        "speaker_id": "MALE_SENIOR_VILLAIN",
        "gender": "male",
        "age_group": "senior",
        "character_name": "김병수 (남편, 70세)",
        "style_prompt": "남성 70대 노년, 가부장적이고 거칠며 쉰 목소리, 고압적인 호통과 버럭 톤",
        "reference_preset": "male_senior_harsh"
    },
    # 아들 김태호 (남성, 40세 중년)
    "김태호": {
        "speaker_id": "MALE_MIDDLE_SON",
        "gender": "male",
        "age_group": "middle",
        "character_name": "김태호 (아들, 40세)",
        "style_prompt": "남성 40대 중년, 기가 죽어 있고 우유부단하며 눈치 보는 힘없는 톤, 후반부 진심 어린 후회와 눈물",
        "reference_preset": "male_middle_meek"
    },
    # 며느리 최윤지 (여성, 38세 청년/중년초반 조력자)
    "최윤지": {
        "speaker_id": "FEMALE_YOUNG_HELPER",
        "gender": "female",
        "age_group": "young_middle",
        "character_name": "최윤지 (며느리, 38세)",
        "style_prompt": "여성 30대 후반, 조용하고 공손하지만 내면에 정의롭고 강단 있는 맑고 또렷한 톤",
        "reference_preset": "female_young_resolute"
    },
    # 법조인: 판사 (남성, 50대 중년)
    "판사": {
        "speaker_id": "MALE_MIDDLE_JUDGE",
        "gender": "male",
        "age_group": "middle",
        "character_name": "판사 (50대)",
        "style_prompt": "남성 50대, 근엄하고 신뢰감 넘치는 표준어 법원 판결 톤",
        "reference_preset": "male_middle_judge"
    },
    # 법조인: 변호사 (남성, 30대 청년)
    "변호사": {
        "speaker_id": "MALE_YOUNG_LAWYER",
        "gender": "male",
        "age_group": "young",
        "character_name": "변호사 (30대)",
        "style_prompt": "남성 30대, 차분하고 전문적인 상담 톤",
        "reference_preset": "male_young_professional"
    },
    # 기타 조연들
    "경찰": {
        "speaker_id": "MALE_YOUNG_OFFICER",
        "gender": "male",
        "age_group": "young",
        "character_name": "경찰",
        "style_prompt": "남성 30대, 무뚝뚝하고 형식적인 어조",
        "reference_preset": "male_young_neutral"
    },
    "노인": {
        "speaker_id": "MALE_SENIOR_EXTRA",
        "gender": "male",
        "age_group": "senior",
        "character_name": "노인 손님",
        "style_prompt": "남성 70대, 소박하고 주름진 노년 어르신 톤",
        "reference_preset": "male_senior_gentle"
    },
    "어르신": {
        "speaker_id": "MALE_SENIOR_EXTRA",
        "gender": "male",
        "age_group": "senior",
        "character_name": "어르신",
        "style_prompt": "남성 70대, 소박하고 주름진 노년 어르신 톤",
        "reference_preset": "male_senior_gentle"
    },
    "어르신1": {
        "speaker_id": "FEMALE_SENIOR_EXTRA",
        "gender": "female",
        "age_group": "senior",
        "character_name": "어르신1",
        "style_prompt": "여성 70대, 따뜻하고 정다운 동네 할머니 톤",
        "reference_preset": "female_senior_warm"
    },
    "어르신2": {
        "speaker_id": "MALE_SENIOR_EXTRA",
        "gender": "male",
        "age_group": "senior",
        "character_name": "어르신2",
        "style_prompt": "남성 70대, 힘없이 감동받은 어르신 톤",
        "reference_preset": "male_senior_gentle"
    },
    "할머니1": {
        "speaker_id": "FEMALE_SENIOR_EXTRA",
        "gender": "female",
        "age_group": "senior",
        "character_name": "할머니1",
        "style_prompt": "여성 70대, 활기찬 동네 할머니 톤",
        "reference_preset": "female_senior_warm"
    },
    "할머니2": {
        "speaker_id": "FEMALE_SENIOR_EXTRA",
        "gender": "female",
        "age_group": "senior",
        "character_name": "할머니2",
        "style_prompt": "여성 70대, 다정한 동네 할머니 톤",
        "reference_preset": "female_senior_warm"
    },
    "봉사자": {
        "speaker_id": "FEMALE_YOUNG_VOLUNTEER",
        "gender": "female",
        "age_group": "young",
        "character_name": "대학생 봉사자",
        "style_prompt": "여성 20대, 밝고 존경을 담은 목소리",
        "reference_preset": "female_young_bright"
    },
    "앵커": {
        "speaker_id": "FEMALE_MIDDLE_ANCHOR",
        "gender": "female",
        "age_group": "middle",
        "character_name": "뉴스 앵커",
        "style_prompt": "여성 40대, 정확하고 또렷한 방송 뉴스 앵커 톤",
        "reference_preset": "female_middle_anchor"
    },
    "기자": {
        "speaker_id": "MALE_YOUNG_REPORTER",
        "gender": "male",
        "age_group": "young",
        "character_name": "기자",
        "style_prompt": "남성 30대, 신속한 현장 기자 톤",
        "reference_preset": "male_young_reporter"
    }
}


def smart_chunk_text(text: str, max_chars: int = 120) -> list[str]:
    """긴 대본 텍스트를 문맥이 끊기지 않게 쉼표, 마침표, 줄바꿈 기준으로 자연스럽게 슬라이싱"""
    text = text.strip()
    if not text:
        return []
    
    # 텍스트가 이미 짧으면 그대로 반환
    if len(text) <= max_chars:
        return [text]
    
    # 문장 단위로 분할
    sentences = re.split(r'(?<=[.?!…~])\s+|\n+', text)
    chunks = []
    current_chunk = ""
    
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        
        if len(current_chunk) + len(s) + 1 <= max_chars:
            if current_chunk:
                current_chunk += " " + s
            else:
                current_chunk = s
        else:
            if current_chunk:
                chunks.append(current_chunk)
            # 만약 한 문장 자체가 max_chars보다 크면 쉼표로 분할
            if len(s) > max_chars:
                sub_parts = re.split(r'(?<=[,])\s+', s)
                sub_curr = ""
                for p in sub_parts:
                    if len(sub_curr) + len(p) + 1 <= max_chars:
                        sub_curr = (sub_curr + " " + p).strip()
                    else:
                        if sub_curr:
                            chunks.append(sub_curr)
                        sub_curr = p
                if sub_curr:
                    current_chunk = sub_curr
                else:
                    current_chunk = ""
            else:
                current_chunk = s
                
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks


def parse_script_file(filepath: str) -> dict:
    """대본 텍스트 파일을 읽어 섹션별, 화자별로 분해"""
    with open(filepath, "r", encoding="utf-8") as f:
        raw_content = f.read()

    # 제목 추출
    title_match = re.search(r"제목:\s*(.+)", raw_content)
    title = title_match.group(1).strip() if title_match else "시니어 사연"

    # 섹션 분할 (🎬 섹션 N ...)
    section_pattern = re.compile(r"🎬\s*섹션\s*(\d+)\s*–\s*([^\n\r]+)")
    splits = list(section_pattern.finditer(raw_content))

    sections = []
    
    for idx, match in enumerate(splits):
        section_num = int(match.group(1))
        section_title = match.group(2).strip()
        start_pos = match.end()
        end_pos = splits[idx + 1].start() if idx + 1 < len(splits) else len(raw_content)
        
        section_body = raw_content[start_pos:end_pos].strip()
        
        # 화자별 대사/지문 추출 정규표현식: [화자명] 대사내용
        # 태그가 없는 문단은 직전 화자 또는 기본 [내레이션]으로 처리
        dialogue_pattern = re.compile(r"\[([^\]]+)\]\s*([^\[]+)")
        dialogue_matches = list(dialogue_pattern.finditer(section_body))
        
        utterances = []
        
        if dialogue_matches:
            # 첫 번째 [화자] 태그 앞에 내용이 있다면 내레이션으로 처리
            first_start = dialogue_matches[0].start()
            if first_start > 0:
                pre_text = section_body[:first_start].strip()
                if pre_text:
                    for chunk in smart_chunk_text(pre_text):
                        utterances.append({
                            "speaker": "내레이션",
                            "voice_info": CHARACTER_VOICE_MAP.get("내레이션"),
                            "text": chunk
                        })
            
            for d_idx, d_match in enumerate(dialogue_matches):
                speaker_raw = d_match.group(1).strip()
                content = d_match.group(2).strip()
                
                # 화자 매핑 확인
                voice_meta = CHARACTER_VOICE_MAP.get(speaker_raw, CHARACTER_VOICE_MAP["내레이션"])
                
                for chunk in smart_chunk_text(content):
                    utterances.append({
                        "speaker": speaker_raw,
                        "voice_info": voice_meta,
                        "text": chunk
                    })
        else:
            # 화자 태그가 없으면 전체를 내레이션으로 처리
            for chunk in smart_chunk_text(section_body):
                utterances.append({
                    "speaker": "내레이션",
                    "voice_info": CHARACTER_VOICE_MAP["내레이션"],
                    "text": chunk
                })

        sections.append({
            "section_id": section_num,
            "section_key": f"section_{section_num:02d}",
            "section_title": section_title,
            "total_utterances": len(utterances),
            "utterances": utterances
        })

    result = {
        "title": title,
        "app_name": "시니어사연 보이스 무료제작기",
        "total_sections": len(sections),
        "character_catalog": CHARACTER_VOICE_MAP,
        "sections": sections
    }
    
    return result


if __name__ == "__main__":
    script_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_story.txt")
    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "parsed_story.json")
    
    if os.path.exists(script_path):
        parsed = parse_script_file(script_path)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        print(f"✓ 파싱 완료! 총 {parsed['total_sections']}개 섹션이 정상 처리되었습니다.")
        print(f"✓ 결과 파일: {out_path}")
    else:
        print(f"대본 파일을 찾을 수 없습니다: {script_path}")
