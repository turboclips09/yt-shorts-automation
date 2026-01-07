import asyncio
import edge_tts
import pathlib

TEXT = pathlib.Path("script.txt").read_text(encoding="utf-8").strip()

VOICE = "en-US-GuyNeural"
RATE = "+8%"
PITCH = "+2Hz"

async def main():
    communicate = edge_tts.Communicate(
        text=TEXT,
        voice=VOICE,
        rate=RATE,
        pitch=PITCH
    )

    audio_chunks = []

    async for event in communicate.stream():
        if event["type"] == "audio":
            audio_chunks.append(event["data"])

    if not audio_chunks:
        raise RuntimeError("❌ No audio received from Edge TTS")

    with open("voice.mp3", "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)

    print("✅ voice.mp3 generated successfully")

asyncio.run(main())
