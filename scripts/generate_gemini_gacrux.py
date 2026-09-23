import os
import requests
import json
import base64
import subprocess
import imageio_ffmpeg
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment!")

sample_text = "그때는 미처 몰랐습니다. 어머니의 닳아빠진 고무신 한 켤레가, 저를 키워낸 전부였다는 것을요. 세월이 흘러 백발이 성성해진 지금에야 비로소 가슴을 칩니다."

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={api_key}"
prompt = f"당신은 감동적인 인생사연을 전문적으로 낭독하는 시니어 유튜브 전문 나레이터입니다. 차분하고 중후하며 마음을 울리는 깊은 어조로 천천히 읽어주세요:\n\n{sample_text}"

payload = {
    "contents": [{
        "parts": [{"text": prompt}]
    }],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
            "voiceConfig": {
                "prebuiltVoiceConfig": {
                    "voiceName": "Gacrux"
                }
            }
        }
    }
}

os.makedirs("output/samples", exist_ok=True)
pcm_path = "output/samples/gacrux_temp.pcm"
out_mp3 = "output/samples/NARRATION_GACRUX.mp3"

print("[Gemini TTS] Requesting Gacrux voice synthesis...")
res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
if res.status_code == 200:
    data = res.json()
    candidates = data.get("candidates", [])
    if candidates:
        parts = candidates[0].get("content", {}).get("parts", [])
        for p in parts:
            if "inlineData" in p:
                b64 = p["inlineData"].get("data")
                raw_bytes = base64.b64decode(b64)
                with open(pcm_path, "wb") as f:
                    f.write(raw_bytes)
                
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                subprocess.run([
                    ffmpeg_exe, "-y",
                    "-f", "s16le", "-ar", "24000", "-ac", "1",
                    "-i", pcm_path,
                    "-b:a", "192k", out_mp3
                ], check=True, capture_output=True)
                
                if os.path.exists(pcm_path):
                    os.remove(pcm_path)
                
                print(f"[Gemini TTS] Success! Generated: {out_mp3} ({os.path.getsize(out_mp3)} bytes)")
                break
    else:
        print("[Gemini TTS] No candidates returned:", data)
else:
    print(f"[Gemini TTS] Error {res.status_code}: {res.text}")
