import asyncio
import edge_tts

VOICE = "en-US-GuyNeural"  # energetic, natural
RATE = "+10%"               # slightly faster = more energy
VOLUME = "+0%"

async def main():
    with open("script.txt", "r", encoding="utf-8") as f:
        text = f.read()

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE,
        volume=VOLUME
    )

    await communicate.save("voice_raw.mp3")

asyncio.run(main())

print("Natural voice generated")
