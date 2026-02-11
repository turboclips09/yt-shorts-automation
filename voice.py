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

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])

        if chunk["type"] == "WordBoundary":
            word_timings.append({
                "word": chunk["text"],
                "start": chunk["offset"] / 10_000_000,
                "end": (chunk["offset"] + chunk["duration"]) / 10_000_000
            })

    if not audio_chunks:
        raise RuntimeError("❌ No audio received")

    with open("voice.mp3", "wb") as f:
        for audio in audio_chunks:
            f.write(audio)

    if not word_timings:
        print("⚠ No word timings received — falling back to proportional timing")
    else:
        with open("word_timings.json", "w") as f:
            json.dump(word_timings, f, indent=2)

    print("✅ voice.mp3 generated")

asyncio.run(main())
