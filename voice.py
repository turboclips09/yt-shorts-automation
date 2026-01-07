import asyncio
import json
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

    words = []
    audio_chunks = []

    async for event in communicate.stream():
        if event["type"] == "audio":
            audio_chunks.append(event["data"])

        elif event["type"] == "WordBoundary":
            words.append({
                "word": event["text"],
                "offset": int(event["offset"] / 10_000),     # ms
                "duration": int(event["duration"] / 10_000) # ms
            })

    if not audio_chunks:
        raise RuntimeError("❌ No audio received from Edge TTS")

    if not words:
        raise RuntimeError("❌ No word boundaries received from Edge TTS")

    # Write audio file
    with open("voice.mp3", "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)

    # Write word timings
    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)

    print(f"✅ voice.mp3 generated ({len(audio_chunks)} audio chunks)")
    print(f"✅ words.json generated ({len(words)} words)")

asyncio.run(main())
