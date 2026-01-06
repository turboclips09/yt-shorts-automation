from moviepy.editor import AudioFileClip, CompositeAudioClip

# Load raw voice and background music
voice = AudioFileClip("voice_raw.mp3")
music = AudioFileClip("assets/bg_music.mp3")

# Lower background music volume
music = music.volumex(0.15)

# Loop music to match voice length
music = music.audio_loop(duration=voice.duration)

# Mix both
final_audio = CompositeAudioClip([music, voice])

# Export final audio
final_audio.write_audiofile("voice.mp3")

print("Final mixed voice created: voice.mp3")
