import asyncio
import json
import edge_tts

TEXT = open("script.txt", "r", encoding="utf-8").read()

async def main():
    communicate = edge_tts.Communicate(
        TEXT,
        voice="en-US-GuyNeural",
        rate="+8%",   # 🔥 faster, as requested
        pitch="+2Hz"
    )

    audio = b""
    words = []

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]

        if chunk["type"] == "WordBoundary":
            words.append({
                "word": chunk["text"],
                "offset": chunk["offset"] / 10_000,   # ms
                "duration": chunk["duration"] / 10_000
            })

    if not words:
        raise Exception("❌ No word boundaries received from Edge TTS")

    with open("voice.mp3", "wb") as f:
        f.write(audio)

    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

    print(f"✅ Voice generated with {len(words)} word timings")

asyncio.run(main())
