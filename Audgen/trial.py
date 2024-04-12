from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_fadein, audio_fadeout
from moviepy.video.fx.all import speedx

def synchronize_audio_video(video_path, audio_path, output_path, audio_delay_duration=1):
    # Load video and audio clips
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Adjust audio and video durations to match
    video_clip, audio_clip = match_durations(video_clip, audio_clip)

    # Add delay to the audio with fade-in effect
    audio_delay_clip = audio_clip.fx(audio_fadein, duration=audio_delay_duration)
    
    # Set audio of the video clip
    video_clip = video_clip.set_audio(audio_delay_clip)

    # Write the synchronized video to a file
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", remove_temp=True)

def match_durations(video_clip, audio_clip):
    # Get the durations of the video and audio clips
    video_duration = video_clip.duration
    audio_duration = audio_clip.duration

    # Determine which clip is shorter
    shorter_duration = min(video_duration, audio_duration)

    # Match durations at the end without fades
    if audio_duration < video_duration:
        speed_ratio = video_duration / (audio_duration+6)
        audio_clip = audio_clip.fx(speedx, speed_ratio)
    elif audio_duration > video_duration:
        speed_ratio = audio_duration / video_duration
        video_clip = video_clip.fx(speedx, speed_ratio)

    return video_clip, audio_clip

if __name__ == "__main__":
    video_path = r"D:\D-KTS\results\tvsum\91IHQYk1IQM\vs_91IHQYk1IQM.mp4"
    audio_path = r"F:\mainproject\WisperAI\output_summary.mp3"
    output_path = "naruto.mp4"

    synchronize_audio_video(video_path, audio_path, output_path, audio_delay_duration=3)
