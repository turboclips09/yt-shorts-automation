import asyncio
import edge_tts
import json

TEXT = open("script.txt", "r", encoding="utf-8").read()

VOICE = "en-US-GuyNeural"
RATE = "+8%"
PITCH = "+2Hz"

async def main():
    communicator = edge_tts.Communicate(
        TEXT,
        VOICE,
        rate=RATE,
        pitch=PITCH
    )

    words = []
    audio_chunks = []

    async for event in communicator.stream():
        if event["type"] == "audio":
            audio_chunks.append(event["data"])

        elif event["type"] == "WordBoundary":
            words.append({
                "word": event["text"],
                "offset": event["offset"],
                "duration": event["duration"]
            })

    # Save audio
    with open("voice.mp3", "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)

    if not words:
        raise Exception("❌ No word boundaries received from Edge TTS")

    # Save word timings
    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)

    print(f"✅ voice.mp3 created")
    print(f"✅ words.json created with {len(words)} words")

asyncio.run(main())
