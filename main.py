import streamlit as st
import subprocess
import os
import shutil
import time

def main():
    st.title("Automated Video Summarization")

    # User input for video file
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

    if uploaded_file is not None:
        st.video(uploaded_file)

        if st.button("Generate Video Summary"):
            # Rename the video file to 'fWutDQy1nnY.mp4'
            new_video_file_name = 'fWutDQy1nnY.mp4'

            # Copy the video file to the destination folder
            destination_folder = 'D:\\ydata-tvsum50-v1_1\\ydata-tvsum50-video\\video'
            destination_path = os.path.join(destination_folder, new_video_file_name)

            # Copy the video file
            with open(destination_path, 'wb') as destination_file:
                destination_file.write(uploaded_file.getvalue())

            st.success(f"Video uploaded successfully! generating video frames..")

            # Run the video summarization and audio processing commands with progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            start_time = time.time()

            run_video_summarization(destination_path, progress_bar, status_text)
            #run_audio_processing(progress_bar, status_text)
            #video_summary_path = run_new_py(progress_bar, status_text)

            end_time = time.time()

            elapsed_time = end_time - start_time
            status_text.success(f"Video summary generated successfully in {elapsed_time:.2f} seconds.")

            # Display the summary video
            #st.video(video_summary_path)
            


def run_video_summarization(video_path, progress_bar, status_text):
    total_steps = 5

    # Command 1
    progress_bar.progress(20)
    subprocess.run(['python', 'feature_extractor.py', '--frequency', '15', '--file', 'tvsum2_googlenet.h5'])

    # Command 2
    progress_bar.progress(40)
    subprocess.run(['python', 'kts_run.py', '--frequency', '15', '--file', 'tvsum2_googlenet.h5'])

    # Navigate to "dsn" directory
    os.chdir('dsn')

    # Command 3
    progress_bar.progress(60)
    subprocess.run(['python', 'main.py', '-d', '../my_data/tvsum2_googlenet.h5', '-s', 'dataset_split/tvsum_splits.json', '-m', 'tvsum', '--gpu', '0', '--save-dir', 'tvsum2', '--verbose'])

    # Navigate back to the original directory
    os.chdir('..')

    # Command 4
    progress_bar.progress(80)
    subprocess.run(['python', 'video2frame.py'])

    # Command 5
    progress_bar.progress(100)
    subprocess.run(['python', 'summary2video.py'])

    status_text.success("Video frames generated. Generating audio...")
'''
def run_audio_processing(progress_bar, status_text):
    total_steps = 3

    # Navigate to "audgen" directory
    os.chdir('audgen')

    # Command 1
    progress_bar.progress(33)
    subprocess.run(['python', 'ext_aud.py'])
    
    os.chdir('aud_text')

    # Command 2
    progress_bar.progress(66)
    subprocess.run(['whisper', 'D:\\D-KTS\\Audgen\\out_aud\\output.mp3', '--model', 'medium'])

    # Navigate back to the original directory
    os.chdir('..')

    # Command 3
    progress_bar.progress(100)
    status_text.success("Audio generated . Merging video and audio...")

def run_new_py(progress_bar, status_text):
    # Run new.py
    subprocess.run(['python', 'new.py'])

    status_text.success("Merging completed..!!")

    # Return the path to the generated summary video
    return 'D:\\D-KTS\\Audgen\\final_vid\\output_vid.mp4'
'''
if __name__ == "__main__":
    main()
