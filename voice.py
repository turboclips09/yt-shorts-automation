import asyncio
import edge_tts

TEXT = open("script.txt", "r", encoding="utf-8").read()

async def main():
    tts = edge_tts.Communicate(
        TEXT,
        voice="en-US-GuyNeural",
        rate="+8%",
        pitch="+2Hz"
    )

    audio = b""
    async for chunk in tts.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]

    with open("voice.mp3", "wb") as f:
        f.write(audio)

    print("✅ Voice generated successfully")

asyncio.run(main())
