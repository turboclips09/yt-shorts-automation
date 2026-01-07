import asyncio
import json
import edge_tts

TEXT = open("script.txt", "r", encoding="utf-8").read().strip()

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

    async for event in communicate.stream():
        if event["type"] == "WordBoundary":
            words.append({
                "word": event["text"],
                "offset": int(event["offset"] / 10000),     # to ms
                "duration": int(event["duration"] / 10000) # to ms
            })

    # Save audio
    await communicate.save("voice.mp3")

    if not words:
        raise RuntimeError("❌ No word boundaries received from Edge TTS")

    # Save word timings
    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)

    print(f"✅ voice.mp3 generated")
    print(f"✅ words.json generated ({len(words)} words)")

asyncio.run(main())
