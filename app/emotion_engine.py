#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시니어사연 보이스 무료제작기 - 감정 극대화 SSML 엔진 (Emotion Engine)
1. 메인 내레이션: Vrew 1위 '송세아' 특유의 차분하고 중후하며 정갈한 라디오 톤 100% 재현
2. 등장인물 감정 표현 극대화:
   - 김병수: 호통(shouting), 분노(angry), 버럭 소리침
   - 이정희: 억눌린 눈물(sad), 법정 단호함(calm), 인생 회복의 미소(cheerful)
   - 김태호: 쩔쩔매는 우유부단(sad 1.2), 통한의 오열과 사과(sad 2.0)
   - 최윤지: 맑고 강단 있는 정의감(calm 1.5), 시어머니를 향한 눈물의 위로(empathetic 1.8)
   - 판사: 쩌렁쩌렁하고 근엄한 법원 선고 톤
"""

import re
import html


def get_speech_config_and_ssml(speaker: str, text: str) -> dict:
    """화자와 대사의 문맥을 정밀 분석하여 극적인 SSML 및 보이스 파라미터를 생성"""
    clean_text = html.escape(text.strip())
    
    # 1. 메인 내레이션: 송세아 목소리 (Vrew 시니어 사연 부동의 1위 전설 톤)
    if speaker == "내레이션":
        voice = "ko-KR-SunHiNeural"
        style = "calm"
        style_degree = "1.2"
        rate = "-5%"    # 송세아 특유의 진중하고 꼭꼭 씹어 발음하는 정갈한 속도
        pitch = "-4Hz"  # 들뜨지 않고 가슴을 울리는 중후하고 편안한 중년 톤
        volume = "+0%"
        
    # 2. 김병수 (남편, 70세 악역) - 감정 표현 극대화!
    elif speaker == "김병수":
        voice = "ko-KR-InJoonNeural"
        # 호통/폭언/버럭
        if any(w in text for w in ["이년아", "말대답", "미쳤어", "너 지금", "그딴 식", "기어오른다"]) or "!" in text:
            style = "shouting"
            style_degree = "2.0"
            pitch = "+5Hz"
            rate = "+6%"
            volume = "+35%"
        # 뻔뻔하고 비아냥거리는 악역 톤
        else:
            style = "angry"
            style_degree = "1.6"
            pitch = "-5Hz"
            rate = "-1%"
            volume = "+15%"

    # 3. 이정희 (주인공, 65세 여) - 슬픔과 연륜, 단호함
    elif speaker in ["이정희", "상상 속 이정희"]:
        voice = "ko-KR-SunHiNeural"
        # 눈물, 슬픔, 억눌린 설움
        if any(w in text for w in ["울었", "눈물", "참았", "아팠", "초라", "두려", "슬퍼"]) or "…" in text:
            style = "sad"
            style_degree = "1.8"
            pitch = "-6Hz"
            rate = "-8%"
            volume = "-5%"
        # 법정에서의 단호함, 결의
        elif any(w in text for w in ["판사님", "참지 않겠습니다", "나 자신", "지키", "선택한"]):
            style = "calm"
            style_degree = "1.6"
            pitch = "-3Hz"
            rate = "-4%"
            volume = "+10%"
        # 후반부 따뜻한 미소와 자존감 회복
        else:
            style = "cheerful"
            style_degree = "1.1"
            pitch = "-2Hz"
            rate = "-3%"
            volume = "+0%"

    # 4. 김태호 (아들, 40세 남) - 우유부단과 오열 사과
    elif speaker == "김태호":
        voice = "ko-KR-InJoonNeural"
        # 통한의 오열, 참회의 눈물
        if any(w in text for w in ["미안해", "울었", "움직이지 못했", "부끄러웠", "응원할께", "용서"]):
            style = "sad"
            style_degree = "2.0"
            pitch = "-4Hz"
            rate = "-7%"
            volume = "+10%"
        # 눈치 보고 쩔쩔맴
        else:
            style = "sad"
            style_degree = "1.2"
            pitch = "-1Hz"
            rate = "-4%"
            volume = "-5%"

    # 5. 최윤지 (며느리, 38세 여) - 맑고 강단 있는 정의감 & 위로
    elif speaker == "최윤지":
        voice = "ko-KR-SunHiNeural"
        # 시어머니를 향한 눈물의 위로, 따뜻한 연대
        if any(w in text for w in ["어머니", "존경", "손을", "가족", "롤모델", "눈물"]):
            style = "empathetic"
            style_degree = "1.8"
            pitch = "+1Hz"
            rate = "-4%"
            volume = "+5%"
        # 증거 제시 및 법적 경고 (단호하고 강단 있는 톤)
        else:
            style = "calm"
            style_degree = "1.6"
            pitch = "+3Hz"
            rate = "+1%"
            volume = "+10%"

    # 6. 법원 판사 (50대 남성) - 근엄한 사법 판결
    elif speaker == "판사":
        voice = "ko-KR-InJoonNeural"
        style = "calm"
        style_degree = "1.8"
        pitch = "-6Hz"
        rate = "-6%"
        volume = "+20%"

    # 7. 변호사 (30대 남성)
    elif speaker == "변호사":
        voice = "ko-KR-InJoonNeural"
        style = "calm"
        style_degree = "1.3"
        pitch = "+0Hz"
        rate = "-2%"
        volume = "+5%"

    # 8. 동네 어르신 / 할머니
    elif any(k in speaker for k in ["어르신", "할머니", "노인"]):
        voice = "ko-KR-SunHiNeural" if "할머니" in speaker or "어르신1" in speaker else "ko-KR-InJoonNeural"
        style = "cheerful"
        style_degree = "1.2"
        pitch = "-5Hz"
        rate = "-8%"
        volume = "+0%"

    # 기타 기본
    else:
        voice = "ko-KR-SunHiNeural"
        style = "calm"
        style_degree = "1.0"
        rate = "-3%"
        pitch = "-2Hz"
        volume = "+0%"

    # W3C 표준 SSML 구조 조립
    ssml = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='ko-KR'>
    <voice name='{voice}'>
        <mstts:express-as style='{style}' styledegree='{style_degree}'>
            <prosody pitch='{pitch}' rate='{rate}' volume='{volume}'>
                {clean_text}
            </prosody>
        </mstts:express-as>
    </voice>
</speak>"""

    return {
        "voice": voice,
        "style": style,
        "style_degree": style_degree,
        "pitch": pitch,
        "rate": rate,
        "volume": volume,
        "ssml": ssml
    }


if __name__ == "__main__":
    test_narration = get_speech_config_and_ssml("내레이션", "추석 명절날 가족이 함께 성묘하러 간 자리였어요.")
    print("✓ 내레이션 (송세아 톤) SSML:\n", test_narration["ssml"])
    
    test_shout = get_speech_config_and_ssml("김병수", "감히 어디서 말대답이야, 이년아!")
    print("\n✓ 김병수 (호통 버럭 톤) SSML:\n", test_shout["ssml"])
