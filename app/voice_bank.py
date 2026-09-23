#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시니어사연 보이스 무료제작기 - 21대 전속 성우 보이스 뱅크 (Voice Actor Bank)
- 메인 내레이션: 송세아 (Vrew 시니어 사연 부동의 1위 라디오 톤)
- 5개 연령대 (어린이, 10대, 20~30대 청년, 40~50대 중년, 60~70대 노년)
- 남성 / 여성 각각 선역(Good) vs 악역(Villain) 완벽 분리
"""

VOICE_BANK = [
    # ==========================================
    # ⭐ 0. 메인 내레이션 (송세아)
    # ==========================================
    {
        "id": "NARRATION_SONGSEAH",
        "name": "송세아 (메인 내레이터)",
        "category": "내레이션",
        "gender": "female",
        "age_group": "중년 (40대)",
        "role_type": "해설",
        "voice": "ko-KR-SunHiNeural",
        "style": "calm",
        "style_degree": "1.2",
        "rate": "-5%",
        "pitch": "-4Hz",
        "volume": "+0%",
        "desc": "Vrew 1위 송세아 특유의 지적이고 차분하며 귀에 착 감기는 듣기 편안한 라디오/오디오북 전용 톤",
        "sample_text": "이야기의 결말이 궁금하시다면, 영상 끝까지 시청해 주세요. 그럼 지금부터 오늘의 사연을 시작하겠습니다."
    },

    # ==========================================
    # 👵👴 1. 노년 (60~70대)
    # ==========================================
    {
        "id": "SENIOR_FEMALE_GOOD",
        "name": "정희 (노년 여성 선역)",
        "category": "노년",
        "gender": "female",
        "age_group": "60~70대",
        "role_type": "선역",
        "voice": "ko-KR-SunHiNeural",
        "style": "sad",
        "style_degree": "1.6",
        "rate": "-7%",
        "pitch": "-6Hz",
        "volume": "+0%",
        "desc": "삶의 연륜과 억눌린 설움, 그러나 단호하고 온화한 어머니/할머니 목소리",
        "sample_text": "30년 동안 가족을 위해 일했는데… 이제는 더 이상 참지 않겠습니다."
    },
    {
        "id": "SENIOR_FEMALE_EVIL",
        "name": "말순 (노년 여성 악역)",
        "category": "노년",
        "gender": "female",
        "age_group": "60~70대",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "style": "angry",
        "style_degree": "1.8",
        "rate": "+2%",
        "pitch": "-2Hz",
        "volume": "+20%",
        "desc": "표독스럽고 깐깐하며 며느리를 구박하는 심술궂은 시어머니 톤",
        "sample_text": "어디서 시어머니 앞에서 눈을 치켜뜨고 대들어? 집안 말아먹을 년 같으니!"
    },
    {
        "id": "SENIOR_MALE_GOOD",
        "name": "만석 (노년 남성 선역)",
        "category": "노년",
        "gender": "male",
        "age_group": "60~70대",
        "role_type": "선역",
        "voice": "ko-KR-InJoonNeural",
        "style": "calm",
        "style_degree": "1.3",
        "rate": "-8%",
        "pitch": "-7Hz",
        "volume": "+0%",
        "desc": "정답고 소박하며 힘없는 착한 시골 어르신/장인어른 목소리",
        "sample_text": "허허, 이 사람아… 머리칼만 다듬은 게 아니라 내 한숨까지 다 잘라내 줬구먼."
    },
    {
        "id": "SENIOR_MALE_EVIL",
        "name": "병수 (노년 남성 악역)",
        "category": "노년",
        "gender": "male",
        "age_group": "60~70대",
        "role_type": "악역",
        "voice": "ko-KR-InJoonNeural",
        "style": "shouting",
        "style_degree": "2.0",
        "rate": "+6%",
        "pitch": "+4Hz",
        "volume": "+35%",
        "desc": "가부장적이고 거칠며 버럭 호통치고 손찌검하는 폭력적 남편 톤",
        "sample_text": "감히 어디서 말대답이야, 이년아! 당장 그 건물 서류 내 명의로 넘겨!"
    },

    # ==========================================
    # 👩👨 2. 중년 (40~50대)
    # ==========================================
    {
        "id": "MIDDLE_FEMALE_GOOD",
        "name": "순영 (중년 여성 선역)",
        "category": "중년",
        "gender": "female",
        "age_group": "40~50대",
        "role_type": "선역",
        "voice": "ko-KR-SunHiNeural",
        "style": "empathetic",
        "style_degree": "1.5",
        "rate": "-3%",
        "pitch": "-2Hz",
        "volume": "+0%",
        "desc": "따뜻하고 속 깊은 동네 아주머니, 헌신적인 친정엄마 목소리",
        "sample_text": "정희야, 그동안 혼자 얼마나 힘들었니… 이제 우리 같이 힘내자."
    },
    {
        "id": "MIDDLE_FEMALE_EVIL",
        "name": "미자 (중년 여성 악역)",
        "category": "중년",
        "gender": "female",
        "age_group": "40~50대",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "style": "angry",
        "style_degree": "1.5",
        "rate": "+4%",
        "pitch": "+3Hz",
        "volume": "+15%",
        "desc": "얄밉고 사치스러우며 남의 불행을 비웃는 밉상 시누이/사기꾼 톤",
        "sample_text": "어머 언니, 꼴랑 그거 벌면서 유세는! 그 나이에 이혼하면 밥은 먹고 사나 몰라?"
    },
    {
        "id": "MIDDLE_MALE_GOOD",
        "name": "성우 (중년 남성 선역/판사)",
        "category": "중년",
        "gender": "male",
        "age_group": "40~50대",
        "role_type": "선역",
        "voice": "ko-KR-InJoonNeural",
        "style": "calm",
        "style_degree": "1.7",
        "rate": "-5%",
        "pitch": "-5Hz",
        "volume": "+15%",
        "desc": "근엄하고 정의로운 법원 판사, 듬직하고 신뢰감 넘치는 표준 톤",
        "sample_text": "본 법원은 피고인의 지속적인 폭행 사실을 인정하며, 유죄를 선고합니다."
    },
    {
        "id": "MIDDLE_MALE_EVIL",
        "name": "태호 (중년 남성 나약/악역)",
        "category": "중년",
        "gender": "male",
        "age_group": "40~50대",
        "role_type": "악역",
        "voice": "ko-KR-InJoonNeural",
        "style": "sad",
        "style_degree": "1.4",
        "rate": "-3%",
        "pitch": "-1Hz",
        "volume": "-5%",
        "desc": "아버지 눈치 보느라 어머니를 외면하는 우유부단하고 비겁한 아들 톤",
        "sample_text": "엄마… 그냥 좀 참으세요. 아버지 화나시는데 왜 자꾸 일을 키워요?"
    },

    # ==========================================
    # 👩‍🦱👨‍🦱 3. 청년 (20~30대)
    # ==========================================
    {
        "id": "YOUNG_FEMALE_GOOD",
        "name": "윤지 (청년 여성 선역)",
        "category": "청년",
        "gender": "female",
        "age_group": "20~30대",
        "role_type": "선역",
        "voice": "ko-KR-SunHiNeural",
        "style": "calm",
        "style_degree": "1.5",
        "rate": "+0%",
        "pitch": "+2Hz",
        "volume": "+5%",
        "desc": "조용하지만 내면에 단단한 정의감을 품은 든든한 며느리/딸 (최윤지)",
        "sample_text": "어머니… 이 영상, 명백한 폭행 증거예요. 이젠 그만 참으셔야 해요."
    },
    {
        "id": "YOUNG_FEMALE_EVIL",
        "name": "수진 (청년 여성 악역)",
        "category": "청년",
        "gender": "female",
        "age_group": "20~30대",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "style": "cheerful",
        "style_degree": "1.8",
        "rate": "+6%",
        "pitch": "+6Hz",
        "volume": "+15%",
        "desc": "싸가지 없고 계산적이며 시어머니를 대놓고 무시하는 얌체 며느리 톤",
        "sample_text": "어머님, 요즘 세상에 누가 그런 구식 방식으로 살아요? 남한테 피해주지 마세요."
    },
    {
        "id": "YOUNG_MALE_GOOD",
        "name": "진우 (청년 남성 선역/변호사)",
        "category": "청년",
        "gender": "male",
        "age_group": "20~30대",
        "role_type": "선역",
        "voice": "ko-KR-InJoonNeural",
        "style": "calm",
        "style_degree": "1.3",
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+5%",
        "desc": "예의 바르고 전문적인 젊은 변호사/청년 봉사자 톤",
        "sample_text": "의뢰인님, 증거가 명백하니 두려워하지 마십시오. 제가 끝까지 지켜드리겠습니다."
    },
    {
        "id": "YOUNG_MALE_EVIL",
        "name": "동현 (청년 남성 악역)",
        "category": "청년",
        "gender": "male",
        "age_group": "20~30대",
        "role_type": "악역",
        "voice": "ko-KR-InJoonNeural",
        "style": "angry",
        "style_degree": "1.7",
        "rate": "+5%",
        "pitch": "+3Hz",
        "volume": "+20%",
        "desc": "건방지고 안하무인이며 부모 재산만 노리는 망나니 자식 톤",
        "sample_text": "아 늙은이가 돈 쥐고 있으면 뭐해요? 당장 사업 밑천이나 내놓으라고요!"
    },

    # ==========================================
    # 👧👦 4. 10대 청소년
    # ==========================================
    {
        "id": "TEEN_FEMALE_GOOD",
        "name": "하은 (10대 여성 선역)",
        "category": "10대",
        "gender": "female",
        "age_group": "10대 청소년",
        "role_type": "선역",
        "voice": "ko-KR-SunHiNeural",
        "style": "cheerful",
        "style_degree": "1.4",
        "rate": "+4%",
        "pitch": "+5Hz",
        "volume": "+0%",
        "desc": "착하고 씩씩하며 할머니를 챙기는 사랑스러운 손녀/여학생 톤",
        "sample_text": "할머니! 오늘 행복살롱 봉사 제가 도와드릴게요. 할머니 손은 마법 손이에요!"
    },
    {
        "id": "TEEN_FEMALE_EVIL",
        "name": "채원 (10대 여성 악역)",
        "category": "10대",
        "gender": "female",
        "age_group": "10대 청소년",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "style": "angry",
        "style_degree": "1.4",
        "rate": "+6%",
        "pitch": "+4Hz",
        "volume": "+10%",
        "desc": "삐딱하고 투덜대며 어른에게 버릇없이 구는 불량 여학생 톤",
        "sample_text": "아 짜증 나게 왜 자꾸 간섭이에요? 할머니가 나한테 해준 게 뭔데요?"
    },
    {
        "id": "TEEN_MALE_GOOD",
        "name": "민수 (10대 남성 선역)",
        "category": "10대",
        "gender": "male",
        "age_group": "10대 청소년",
        "role_type": "선역",
        "voice": "ko-KR-InJoonNeural",
        "style": "calm",
        "style_degree": "1.2",
        "rate": "+2%",
        "pitch": "+3Hz",
        "volume": "+0%",
        "desc": "순수하고 성실하며 어른을 공경하는 착한 남학생 톤",
        "sample_text": "할머니, 무거운 짐 제가 들어드릴게요. 감기 조심하세요!"
    },
    {
        "id": "TEEN_MALE_EVIL",
        "name": "준호 (10대 남성 악역)",
        "category": "10대",
        "gender": "male",
        "age_group": "10대 청소년",
        "role_type": "악역",
        "voice": "ko-KR-InJoonNeural",
        "style": "shouting",
        "style_degree": "1.5",
        "rate": "+7%",
        "pitch": "+5Hz",
        "volume": "+15%",
        "desc": "거칠고 반항적이며 길거리에서 시비 거는 불량 남학생 톤",
        "sample_text": "뭐야 이 노인네는? 길 막지 말고 비켜요, 확 그냥!"
    },

    # ==========================================
    # 👶 5. 어린이 (유아/초등)
    # ==========================================
    {
        "id": "CHILD_FEMALE_GOOD",
        "name": "서연 (어린이 여성 선역)",
        "category": "어린이",
        "gender": "female",
        "age_group": "어린이",
        "role_type": "선역",
        "voice": "ko-KR-SunHiNeural",
        "style": "cheerful",
        "style_degree": "1.8",
        "rate": "+8%",
        "pitch": "+9Hz",
        "volume": "+5%",
        "desc": "애교 많고 해맑은 귀여운 꼬마 손녀딸 톤",
        "sample_text": "할머니~ 보고 싶었어요! 제가 예쁘게 안아줄게요, 사랑해요!"
    },
    {
        "id": "CHILD_FEMALE_EVIL",
        "name": "예나 (어린이 여성 악역)",
        "category": "어린이",
        "gender": "female",
        "age_group": "어린이",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "style": "angry",
        "style_degree": "1.6",
        "rate": "+9%",
        "pitch": "+8Hz",
        "volume": "+15%",
        "desc": "발을 동동 구르며 떼쓰고 심술부리는 말썽꾸러기 톤",
        "sample_text": "싫어 싫어! 내 마음대로 할 거야! 할머니 미워, 저리 가!"
    },
    {
        "id": "CHILD_MALE_GOOD",
        "name": "도윤 (어린이 남성 선역)",
        "category": "어린이",
        "gender": "male",
        "age_group": "어린이",
        "role_type": "선역",
        "voice": "ko-KR-InJoonNeural",
        "style": "cheerful",
        "style_degree": "1.6",
        "rate": "+7%",
        "pitch": "+8Hz",
        "volume": "+5%",
        "desc": "씩씩하고 명랑한 장난꾸러기 어린 손자 톤",
        "sample_text": "할머니, 제가 커서 돈 많이 벌어서 큰 집 사드릴게요!"
    },
    {
        "id": "CHILD_MALE_EVIL",
        "name": "시우 (어린이 남성 악역)",
        "category": "어린이",
        "gender": "male",
        "age_group": "어린이",
        "role_type": "악역",
        "voice": "ko-KR-InJoonNeural",
        "style": "shouting",
        "style_degree": "1.7",
        "rate": "+8%",
        "pitch": "+9Hz",
        "volume": "+20%",
        "desc": "소리 지르고 장난감을 던지며 억지 부리는 떼쟁이 톤",
        "sample_text": "내 장난감 내놔! 다 부숴버릴 거야! 으앙!"
    }
]

# ID 기반 빠른 검색 맵
VOICE_BANK_MAP = {v["id"]: v for v in VOICE_BANK}


def get_voice_by_id(voice_id: str) -> dict:
    return VOICE_BANK_MAP.get(voice_id, VOICE_BANK[0])
