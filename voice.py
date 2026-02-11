import asyncio
import edge_tts
import pathlib
import json

TEXT = pathlib.Path("script.txt").read_text(encoding="utf-8").strip()

VOICE = "en-US-GuyNeural"
RATE = "+20%"
PITCH = "+5Hz"

async def main():
    communicate = edge_tts.Communicate(
        text=TEXT,
        voice=VOICE,
        rate=RATE,
        pitch=PITCH
    )

    audio_chunks = []
    word_timings = []

    async for event in communicate.stream():
        if event["type"] == "audio":
            audio_chunks.append(event["data"])

        if event["type"] == "WordBoundary":
            word_timings.append({
                "word": event["text"],
                "start": event["offset"] / 10_000_000,
                "duration": event["duration"] / 10_000_000
            })

    if not audio_chunks:
        raise RuntimeError("❌ No audio received")

    with open("voice.mp3", "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)

    # Save word timing
    with open("word_timings.json", "w") as f:
        json.dump(word_timings, f, indent=2)

    print("✅ voice.mp3 generated")
    print("✅ word_timings.json generated")

asyncio.run(main())
