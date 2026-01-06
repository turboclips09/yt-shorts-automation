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
    await tts.save(
        "voice.mp3",
        word_boundary_path="words.json"
    )

asyncio.run(main())
