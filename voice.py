import asyncio
import json
import edge_tts

TEXT = open("script.txt", "r", encoding="utf-8").read()

async def main():
    communicate = edge_tts.Communicate(
        TEXT,
        voice="en-US-GuyNeural",
        rate="+6%",
        pitch="+2Hz"
    )

    words = []
    audio = b""

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]

        elif chunk["type"] == "WordBoundary":
            words.append({
                "word": chunk["text"],
                "offset": chunk["offset"] / 10_000,   # to ms
                "duration": chunk["duration"] / 10_000
            })

    with open("voice.mp3", "wb") as f:
        f.write(audio)

    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

    print("Voice + word timings generated")

asyncio.run(main())
