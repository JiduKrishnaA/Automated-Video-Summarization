import pyttsx3
from pydub import AudioSegment
import os

def text_to_speech(input_text, output_file, speaking_rate=150, voice_id=None):
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

if __name__ == "__main__":
    input_file = r"F:/mainproject/WisperAI/out_summ/output_summary.txt"  # Use "r" before the string to handle backslashes
    output_file = "output_summary.mp3"

    with open(input_file, "r") as file:
        input_text = file.read()

    # Adjust speaking_rate and voice_id as needed
    speaking_rate = 150  # You can adjust the speed (words per minute)
    voice_id = 0  # Use None for the default voice, or specify an index for a particular voice

    text_to_speech(input_text, output_file, speaking_rate, voice_id)

    print(f"Text converted to audio and saved as {output_file}")
