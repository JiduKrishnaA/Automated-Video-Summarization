from moviepy.editor import VideoFileClip

def extract_audio(video_path, output_path):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Extract audio
    audio_clip = video_clip.audio

    # Save the audio to the specified output path
    audio_clip.write_audiofile(output_path)

    # Close the video clip
    video_clip.close()

# Specify the path to the input video file
input_video_path = r"D:\ydata-tvsum50-v1_1\ydata-tvsum50-video\video\fWutDQy1nnY.mp4"
# Specify the path for the output audio file (e.g., output.mp3)
output_audio_path = 'out_aud/output.mp3'

# Extract audio from the video
extract_audio(input_video_path, output_audio_path)
