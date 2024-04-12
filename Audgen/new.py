from summarizer import Summarizer
import pyttsx3
from pydub import AudioSegment
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_fadein, audio_fadeout
from moviepy.video.fx.all import speedx

def count_sentences_in_text(text_content):
    # Counting the number of sentences in the text content
    return text_content.count('.') + text_content.count('!') + text_content.count('?')

def summarize_and_convert_to_audio(input_path, output_audio_path):
    # Read text file
    with open(input_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Count the number of sentences in the text content
    num_sentences_in_text = count_sentences_in_text(text_content)

    # Calculate the number of sentences for the summary (15% of the total sentences)
    num_sentences_in_summary = int(0.07 * num_sentences_in_text)

    # Use bert-extractive-summarizer to summarize the text content
    summarizer = Summarizer()
    summarized_text = summarizer(text_content, num_sentences=num_sentences_in_summary)

    # Convert summarized text to audio
    text_to_speech(summarized_text, output_audio_path)

def text_to_speech(input_text, output_file, speaking_rate=150, voice_id=0):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set speaking rate (speed)
    engine.setProperty('rate', speaking_rate)

    # Set voice (if voice_id is provided)
    if voice_id:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_id].id)

    # Save the speech to a temporary WAV file
    temp_wav_file = "temp.wav"
    engine.save_to_file(input_text, temp_wav_file)
    engine.runAndWait()

    # Load the WAV file using pydub
    sound = AudioSegment.from_wav(temp_wav_file)

    # Export the audio to MP3 format
    sound.export(output_file, format="mp3")

    # Clean up the temporary WAV file
    os.remove(temp_wav_file)

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
    # Specify the path to the input text file
    input_text_path = r'D:\D-KTS\Audgen\aud_text\output.txt'

    # Specify the path for the output audio file
    output_audio_path = 'output_summary.mp3'

    # Summarize the text content and convert to audio
    summarize_and_convert_to_audio(input_text_path, output_audio_path)

    # Specify the paths for video, audio, and output video
    video_path = r"D:\D-KTS\results\tvsum\fWutDQy1nnY\vs_fWutDQy1nnY.mp4"
    audio_path = r"D:\D-KTS\Audgen\output_summary.mp3"
    output_path = r'D:\\D-KTS\\Audgen\\final_vid\\output_vid.mp4'

    # Synchronize audio and video
    synchronize_audio_video(video_path, audio_path, output_path, audio_delay_duration=3)
