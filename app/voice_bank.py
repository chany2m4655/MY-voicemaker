#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시니어사연 보이스 무료제작기 - 21대 전속 성우 보이스 뱅크 (순수 파라미터 엔진)
edge-tts의 rate, pitch, volume을 정밀 조율하여 XML 태그 없이 순수 고음질 한국어 음성 출력!
"""

VOICE_BANK = [
    # ==========================================
    # ⭐ 0. 메인 내레이션 (송세아 1위 라디오 톤)
    # ==========================================
    {
        "id": "NARRATION_SONGSEAH",
        "name": "송세아 (메인 내레이터)",
        "category": "내레이션",
        "gender": "female",
        "age_group": "중년 (40대)",
        "role_type": "해설",
        "voice": "ko-KR-SunHiNeural",
        "rate": "-5%",
        "pitch": "-4Hz",
        "volume": "+0%",
        "desc": "Vrew 1위 송세아 특유의 지적이고 차분하며 편안한 라디오/오디오북 낭독 톤",
        "sample_text": "이야기의 결말이 궁금하시다면, 영상 끝까지 시청해 주세요. 그럼 지금부터, 오늘의 사연을 시작하겠습니다."
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
        "rate": "-7%",
        "pitch": "-6Hz",
        "volume": "-2%",
        "desc": "삶의 연륜과 억눌린 설움, 그러나 단호하고 온화한 어머니/할머니 목소리",
        "sample_text": "30년 동안 가족을 위해 가위질을 해왔는데… 이제는 더 이상 참지 않겠습니다."
    },
    {
        "id": "SENIOR_FEMALE_EVIL",
        "name": "말순 (노년 여성 악역)",
        "category": "노년",
        "gender": "female",
        "age_group": "60~70대",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "rate": "+4%",
        "pitch": "+2Hz",
        "volume": "+15%",
        "desc": "표독스럽고 깐깐하며 며느리를 구박하는 심술궂은 시어머니 톤",
        "sample_text": "어디서 시어머니 앞에서 눈을 치켜뜨고 대들어?! 집안 말아먹을 년 같으니라고!"
    },
    {
        "id": "SENIOR_MALE_GOOD",
        "name": "만석 (노년 남성 선역)",
        "category": "노년",
        "gender": "male",
        "age_group": "60~70대",
        "role_type": "선역",
        "voice": "ko-KR-InJoonNeural",
        "rate": "-9%",
        "pitch": "-7Hz",
        "volume": "+0%",
        "desc": "정답고 소박하며 힘없는 착한 시골 어르신/장인어른 목소리",
        "sample_text": "허허, 이 사람아… 머리만 다듬은 게 아니라 내 한숨까지 다 잘라내 줬구먼. 고마워요."
    },
    {
        "id": "SENIOR_MALE_EVIL",
        "name": "병수 (노년 남성 악역)",
        "category": "노년",
        "gender": "male",
        "age_group": "60~70대",
        "role_type": "악역",
        "voice": "ko-KR-InJoonNeural",
        "rate": "+6%",
        "pitch": "+5Hz",
        "volume": "+35%",
        "desc": "가부장적이고 거칠며 버럭 호통치는 폭력적 남편 톤 (김병수)",
        "sample_text": "감히 어디서 말대답이야, 이년아!! 당장 그 건물 서류 내 명의로 넘겨!"
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
        "rate": "-3%",
        "pitch": "-2Hz",
        "volume": "+0%",
        "desc": "따뜻하고 속 깊은 동네 아주머니, 헌신적인 친정엄마 목소리",
        "sample_text": "정희야, 그동안 혼자 얼마나 힘들었니… 진작 말하지 그랬어. 이제 우리 같이 힘내자."
    },
    {
        "id": "MIDDLE_FEMALE_EVIL",
        "name": "미자 (중년 여성 악역)",
        "category": "중년",
        "gender": "female",
        "age_group": "40~50대",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "rate": "+5%",
        "pitch": "+4Hz",
        "volume": "+15%",
        "desc": "얄밉고 사치스러우며 남의 불행을 비웃는 밉상 시누이/사기꾼 톤",
        "sample_text": "어머 언니, 꼴랑 그거 벌면서 무슨 유세야? 그 나이에 이혼하면 밥은 먹고 사나 몰라?"
    },
    {
        "id": "MIDDLE_MALE_GOOD",
        "name": "성우 (중년 남성 선역/판사)",
        "category": "중년",
        "gender": "male",
        "age_group": "40~50대",
        "role_type": "선역",
        "voice": "ko-KR-InJoonNeural",
        "rate": "-6%",
        "pitch": "-5Hz",
        "volume": "+15%",
        "desc": "근엄하고 정의로운 법원 판사, 듬직하고 신뢰감 넘치는 표준 톤",
        "sample_text": "본 법원은, 피고인의 지속적인 폭력과 재산 강탈 시도를 인정하며, 유죄를 선고합니다."
    },
    {
        "id": "MIDDLE_MALE_EVIL",
        "name": "태호 (중년 남성 나약/악역)",
        "category": "중년",
        "gender": "male",
        "age_group": "40~50대",
        "role_type": "악역",
        "voice": "ko-KR-InJoonNeural",
        "rate": "-4%",
        "pitch": "-2Hz",
        "volume": "-5%",
        "desc": "아버지 눈치 보느라 어머니를 외면하는 우유부단하고 비겁한 아들 톤 (김태호)",
        "sample_text": "엄마… 그냥 좀 참으세요. 아버지 화나시는데 왜 자꾸 일을 이렇게 크게 키워요?"
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
        "rate": "+0%",
        "pitch": "+2Hz",
        "volume": "+5%",
        "desc": "조용하지만 내면에 단단한 정의감을 품은 든든한 며느리 (최윤지)",
        "sample_text": "어머니… 이 영상, 명백한 폭행 증거예요. 지금 아니면 영영 안 바뀌어요. 그만 참으세요."
    },
    {
        "id": "YOUNG_FEMALE_EVIL",
        "name": "수진 (청년 여성 악역)",
        "category": "청년",
        "gender": "female",
        "age_group": "20~30대",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "rate": "+7%",
        "pitch": "+6Hz",
        "volume": "+15%",
        "desc": "싸가지 없고 계산적이며 시어머니를 대놓고 무시하는 얌체 며느리 톤",
        "sample_text": "어머님, 요즘 세상에 누가 그런 구식으로 살아요? 제발 남한테 민폐 좀 끼치지 마세요."
    },
    {
        "id": "YOUNG_MALE_GOOD",
        "name": "진우 (청년 남성 선역/변호사)",
        "category": "청년",
        "gender": "male",
        "age_group": "20~30대",
        "role_type": "선역",
        "voice": "ko-KR-HyunsuMultilingualNeural",
        "rate": "-1%",
        "pitch": "+0Hz",
        "volume": "+5%",
        "desc": "예의 바르고 전문적인 젊은 변호사/청년 봉사자 톤",
        "sample_text": "이정희 선생님, 증거가 너무나 명백합니다. 두려워하지 마세요, 저희가 끝까지 지켜드립니다."
    },
    {
        "id": "YOUNG_MALE_EVIL",
        "name": "동현 (청년 남성 악역)",
        "category": "청년",
        "gender": "male",
        "age_group": "20~30대",
        "role_type": "악역",
        "voice": "ko-KR-HyunsuMultilingualNeural",
        "rate": "+6%",
        "pitch": "+4Hz",
        "volume": "+20%",
        "desc": "건방지고 안하무인이며 부모 재산만 노리는 망나니 자식 톤",
        "sample_text": "아 늙은이가 돈 쥐고 있으면 뭐해요? 당장 제 사업 밑천으로 통장 내놓으라고요!"
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
        "rate": "+5%",
        "pitch": "+5Hz",
        "volume": "+0%",
        "desc": "착하고 씩씩하며 할머니를 챙기는 사랑스러운 손녀/여학생 톤",
        "sample_text": "할머니! 오늘 행복살롱 미용 봉사 제가 도와드릴게요. 우리 할머니 손은 마법 손이에요!"
    },
    {
        "id": "TEEN_FEMALE_EVIL",
        "name": "채원 (10대 여성 악역)",
        "category": "10대",
        "gender": "female",
        "age_group": "10대 청소년",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "rate": "+7%",
        "pitch": "+5Hz",
        "volume": "+10%",
        "desc": "삐딱하고 투덜대며 어른에게 버릇없이 구는 불량 여학생 톤",
        "sample_text": "아 진짜 짜증 나게 왜 자꾸 간섭인데요? 할머니가 나한테 보태준 거 있어요?"
    },
    {
        "id": "TEEN_MALE_GOOD",
        "name": "민수 (10대 남성 선역)",
        "category": "10대",
        "gender": "male",
        "age_group": "10대 청소년",
        "role_type": "선역",
        "voice": "ko-KR-HyunsuMultilingualNeural",
        "rate": "+3%",
        "pitch": "+3Hz",
        "volume": "+0%",
        "desc": "순수하고 성실하며 어른을 공경하는 착한 남학생 톤",
        "sample_text": "할머니, 무거운 장바구니 제가 들어드릴게요. 날씨 추운데 조심해서 들어가세요!"
    },
    {
        "id": "TEEN_MALE_EVIL",
        "name": "준호 (10대 남성 악역)",
        "category": "10대",
        "gender": "male",
        "age_group": "10대 청소년",
        "role_type": "악역",
        "voice": "ko-KR-HyunsuMultilingualNeural",
        "rate": "+8%",
        "pitch": "+6Hz",
        "volume": "+20%",
        "desc": "거칠고 반항적이며 길거리에서 시비 거는 불량 남학생 톤",
        "sample_text": "뭐야 이 노인네는? 길 막지 말고 팍 비켜요, 확 그냥!"
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
        "rate": "+8%",
        "pitch": "+9Hz",
        "volume": "+5%",
        "desc": "애교 많고 해맑은 귀여운 꼬마 손녀딸 톤",
        "sample_text": "할머니~ 너무너무 보고 싶었어요! 제가 예쁘게 꼭 안아줄게요, 사랑해요!"
    },
    {
        "id": "CHILD_FEMALE_EVIL",
        "name": "예나 (어린이 여성 악역)",
        "category": "어린이",
        "gender": "female",
        "age_group": "어린이",
        "role_type": "악역",
        "voice": "ko-KR-SunHiNeural",
        "rate": "+9%",
        "pitch": "+8Hz",
        "volume": "+15%",
        "desc": "발을 동동 구르며 떼쓰고 심술부리는 말썽꾸러기 톤",
        "sample_text": "싫어 싫어! 내 마음대로 할 거야! 할머니 정말 미워, 저리 가!"
    },
    {
        "id": "CHILD_MALE_GOOD",
        "name": "도윤 (어린이 남성 선역)",
        "category": "어린이",
        "gender": "male",
        "age_group": "어린이",
        "role_type": "선역",
        "voice": "ko-KR-InJoonNeural",
        "rate": "+7%",
        "pitch": "+8Hz",
        "volume": "+5%",
        "desc": "씩씩하고 명랑한 장난꾸러기 어린 손자 톤",
        "sample_text": "할머니, 제가 얼른 어른이 돼서 돈 많이 벌어 큰 집 꼭 사드릴게요!"
    },
    {
        "id": "CHILD_MALE_EVIL",
        "name": "시우 (어린이 남성 악역)",
        "category": "어린이",
        "gender": "male",
        "age_group": "어린이",
        "role_type": "악역",
        "voice": "ko-KR-InJoonNeural",
        "rate": "+9%",
        "pitch": "+9Hz",
        "volume": "+20%",
        "desc": "소리 지르고 장난감을 던지며 억지 부리는 떼쟁이 톤",
        "sample_text": "내 장난감 당장 내놔! 다 부숴버릴 거야! 으앙!"
    }
]

VOICE_BANK_MAP = {v["id"]: v for v in VOICE_BANK}

def get_voice_by_id(voice_id: str) -> dict:
    return VOICE_BANK_MAP.get(voice_id, VOICE_BANK[0])
