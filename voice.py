import asyncio
import edge_tts
import subprocess
import json

TEXT = open("script.txt", "r", encoding="utf-8").read()

VOICE = "en-US-GuyNeural"
RATE = "+8%"
PITCH = "+2Hz"

async def main():
    tts = edge_tts.Communicate(
        TEXT,
        VOICE,
        rate=RATE,
        pitch=PITCH
    )

    await tts.save("voice.mp3")

    # Get duration
    probe = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            "voice.mp3"
        ],
        capture_output=True,
        text=True
    )

    duration = float(probe.stdout.strip())

    # Save metadata for captions
    meta = {
        "duration": duration,
        "rate": RATE,
        "voice": VOICE
    }

    with open("voice_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"✅ voice.mp3 created ({duration:.2f}s)")
    print("⚠️ Word boundaries unavailable — using perceptual sync")

asyncio.run(main())
