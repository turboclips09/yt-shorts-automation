from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import Resize
import os

# Load audio
audio = AudioFileClip("voice.mp3")

clips = []
for file in sorted(os.listdir("clips")):
    if file.endswith(".mp4"):
        clip = VideoFileClip(os.path.join("clips", file))
        clip = clip.fx(Resize, height=1920)
        clip = clip.crop(width=1080, height=1920, x_center=clip.w / 2, y_center=clip.h / 2)
        clips.append(clip)

# Loop clips to match audio length
final_video = concatenate_videoclips(clips, method="compose")
final_video = final_video.subclip(0, audio.duration)

final_video = final_video.set_audio(audio)

final_video.write_videofile(
    "short.mp4",
    codec="libx264",
    audio_codec="aac",
    fps=30
)

print("Final short video created")
