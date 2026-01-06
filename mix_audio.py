from moviepy import AudioFileClip, CompositeAudioClip
from moviepy.audio.fx import MultiplyVolume, AudioLoop

# Load raw voice and background music
voice = AudioFileClip("voice_raw.mp3")
music = AudioFileClip("assets/bg_music.mp3")

# Lower background music volume (15%)
music = music.with_effects([MultiplyVolume(0.15)])

# Loop background music to match voice duration
music = music.with_effects([AudioLoop(duration=voice.duration)])

# Mix voice and background music
final_audio = CompositeAudioClip([music, voice])

# Export final audio
final_audio.write_audiofile("voice.mp3", codec="mp3")

print("Final mixed voice created: voice.mp3")
