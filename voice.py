import asyncio
import edge_tts

TEXT = open("script.txt", "r", encoding="utf-8").read()

async def main():
    communicate = edge_tts.Communicate(
        TEXT,
        voice="en-US-GuyNeural",
        rate="+6%",
        pitch="+2Hz"
    )

    await communicate.save(
        "voice.mp3",
        word_boundary_path="words.json"
    )

asyncio.run(main())
