import cv2
import os
import h5py
from time import time
import shutil

def one_output():
    hdf5_path = r"D:\D-KTS\DSN\models\tvsum2\result4.h5"
    output_folder_base = 'results/tvsum/'

    with h5py.File(hdf5_path, 'a') as f:
        for key in f.keys():
            if key != 'mean_fm':
                video_path = 'D:/ydata-tvsum50-v1_1/ydata-tvsum50-video/video/' + key
                output_folder = output_folder_base + key[:11] + '/frames/'

                # Remove existing output folder if it already exists
                if os.path.exists(output_folder):
                    shutil.rmtree(output_folder)

                os.makedirs(output_folder)

                machine_summary = f[key + '/machine_summary'][()]
                start_time = time()

                camera = cv2.VideoCapture(video_path)
                times = 0

                while True:
                    res, image = camera.read()
                    if not res:
                        print(times)
                        break
                    if machine_summary[times] == 1:
                        frame_name = str(times).zfill(6) + '.jpg'
                        frame_path = os.path.join(output_folder, frame_name)
                        cv2.imwrite(frame_path, image)
                    times += 1

                end_time = time()

                dataset_name = key + '/time4.1'
                if dataset_name in f:
                    # Dataset already exists, update its data
                    f[dataset_name][()] = end_time - start_time
                else:
                    # Dataset doesn't exist, create a new one
                    f.create_dataset(dataset_name, data=end_time - start_time)

                print(end_time - start_time)

if __name__ == "__main__":
    one_output()
