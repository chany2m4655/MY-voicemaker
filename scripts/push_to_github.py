#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 리포지토리 생성 및 자동 푸시 스크립트
"""

import os
import sys
import subprocess
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_NAME = "MY-voicemaker"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "VoiceMaker-Agent"
}

# 1. 사용자 정보 확인
print("▶ 1. GitHub 사용자 정보 확인 중...")
res = requests.get("https://api.github.com/user", headers=headers)
if res.status_code != 200:
    print(f"✗ 인증 실패: {res.status_code} {res.text}")
    sys.exit(1)

user_data = res.json()
username = user_data["login"]
print(f"✓ GitHub 사용자 확인: {username} ({user_data.get('name', '')})")

# 2. 리포지토리 존재 여부 확인 및 생성
print(f"▶ 2. '{REPO_NAME}' 리포지토리 생성 확인 중...")
repo_res = requests.get(f"https://api.github.com/repos/{username}/{REPO_NAME}", headers=headers)
if repo_res.status_code == 404:
    create_payload = {
        "name": REPO_NAME,
        "description": "시니어사연 보이스 무료제작기 - AI 1인 기업 대표님을 위한 100% 무료 시니어 사연 라디오 오디오북 스튜디오",
        "private": False,
        "auto_init": False
    }
    create_res = requests.post("https://api.github.com/user/repos", headers=headers, json=create_payload)
    if create_res.status_code in [201, 200]:
        print(f"✓ 새 리포지토리 '{REPO_NAME}' 생성 성공!")
    else:
        print(f"✗ 리포지토리 생성 오류: {create_res.status_code} {create_res.text}")
        sys.exit(1)
else:
    print(f"✓ 이미 존재하는 리포지토리 '{REPO_NAME}' 확인 완료!")

# 3. Git remote 및 브랜치 설정
print("▶ 3. Git 커밋 및 원격 저장소 푸시 준비 중...")
remote_url = f"https://{TOKEN}@github.com/{username}/{REPO_NAME}.git"

# 현재 디렉토리 기준 git add
subprocess.run(["git", "add", "app/", "scripts/", "data/", "colab/", "output/samples/", "output/section_00/"], check=False)
subprocess.run(["git", "status"], check=False)

commit_msg = "feat: 시니어사연 보이스 무료제작기 v1.0 (21대 성우 뱅크, 송세아 내레이션, MP3 ID3v2 SYLT 싱크, 코랩 T4 워커 탑재)"
subprocess.run(["git", "commit", "-m", commit_msg], check=False)

# remote origin 교체
subprocess.run(["git", "remote", "remove", "origin"], check=False)
subprocess.run(["git", "remote", "add", "origin", remote_url], check=False)
subprocess.run(["git", "branch", "-M", "main"], check=False)

print("▶ 4. GitHub main 브랜치로 푸시 시작...")
push_res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], capture_output=True, text=True)
if push_res.returncode == 0:
    print("\n" + "="*60)
    print(f"🎉 성공적으로 GitHub에 푸시되었습니다!")
    print(f"👉 리포지토리 주소: https://github.com/{username}/{REPO_NAME}")
    print("="*60)
else:
    print(f"✗ 푸시 중 알림:\n{push_res.stderr}\n{push_res.stdout}")
