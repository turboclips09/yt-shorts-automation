import asyncio
import edge_tts
import json

TEXT = open("script.txt", "r", encoding="utf-8").read()

words = []

async def main():
    communicate = edge_tts.Communicate(
        TEXT,
        voice="en-US-GuyNeural",
        rate="+6%",
        pitch="+2Hz"
    )

    with open("voice.mp3", "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append({
                    "word": chunk["text"],
                    "offset": int(chunk["offset"] / 10000),   # to ms
                    "duration": int(chunk["duration"] / 10000)
                })

    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)

    print("✅ voice.mp3 and words.json generated")

asyncio.run(main())
