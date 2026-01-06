from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import Resize, Crop
import os

# Load final audio
audio = AudioFileClip("voice.mp3")

clips = []

for file in sorted(os.listdir("clips")):
    if file.endswith(".mp4"):
        clip = VideoFileClip(os.path.join("clips", file))

        # Apply resize + center crop using MoviePy v2 effects
        clip = clip.with_effects([
            Resize(height=1920),
            Crop(
                width=1080,
                height=1920,
                x_center=clip.w / 2,
                y_center=clip.h / 2
            )
        ])

        clips.append(clip)

# Concatenate clips
final_video = concatenate_videoclips(clips, method="compose")

# Trim video to match audio duration
final_video = final_video.subclip(0, audio.duration)

# Attach audio
final_video = final_video.with_audio(audio)

# Export final short
final_video.write_videofile(
    "short.mp4",
    codec="libx264",
    audio_codec="aac",
    fps=30
)

print("Final short video created: short.mp4")
