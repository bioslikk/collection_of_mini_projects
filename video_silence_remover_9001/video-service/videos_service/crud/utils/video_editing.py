import os
import scipy.io.wavfile
import subprocess
from pymongo import MongoClient
import numpy as np
import time


def cut_video(metadata):
    # just connecting to mongo so that we can update our progress
    MONGO_HOST = os.environ.get('MONGO_HOST', "localhost")
    MONGO_PORT = os.environ.get('MONGO_PORT', "27017")
    mongo = MongoClient('mongodb://{}:{}/vsr'.format(MONGO_HOST, MONGO_PORT))
    metadata['converted_path'] = os.path.join(
        os.environ.get('NFS_DIR', '/tmp'),
        '{}.{}.{}'.format('cutted', str(metadata['_id']), metadata['filename']))
    # -------------------------------------------------------------------------------------
    # ---------------------------- CONVERSION STUFF GOES HERE  ----------------------------
    # -------------------------------------------------------------------------------------
    # ------------------------ 1  USING FFMPEG for SOUND EXTRACTION  ----------------------
    increment_steps(mongo, metadata, 'Extracting sound..')
    # Chose 44.1Hz as our frame rate because it is a common sampling frequency
    result = subprocess.call('ffmpeg -i ' + metadata['path'] + ' -ab 160k -ac 2 -ar 44100 -vn ' + metadata['path'] + '.wav',
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # if ffmpeg failed we finish the process
    if result == 1:
        metadata['stepsCompleted'] = metadata['totalSteps']
        metadata['current_state'] = 'Error in sound extraction'
        update_progress(mongo, metadata)
        return metadata
    # -------------------------------------------------------------------------------------
    # ------------------------ 2 DETECTING SOUND PARTS WITH SCIPY  ------------------------
    increment_steps(mongo, metadata, 'Detecting the silent parts..')
    silence_array = silence_detection(metadata['path'] + '.wav')
    # -------------------------------------------------------------------------------------
    # ------------------------ 3 CREATING INTERVALS FOR THE CUTTING -----------------------
    increment_steps(mongo, metadata, 'Creating time intervals for the cutting..')
    noise_intervals = get_noise_interval(silence_array)
    # This function creates a caption for our where we can see where the parts with noise are
    metadata['noises'] = write_noise_srt(noise_intervals, metadata['path'])
    # -------------------------------------------------------------------------------------
    # ------------------------ 4 USING VIDEOGREP TO CREATE THE CUTTED VIDEO FILE  ---------
    # insert here a function that receives the silence_array and writes a .srt with the intervals
    increment_steps(mongo, metadata, 'Creating a new video file with the noisy parts (this step can take a while)..')
    # https://github.com/antiboredom/videogrep
    result = subprocess.call("videogrep --input {} --output {} --search 'NOISE' --search-type re".format(
        metadata['path'], metadata['converted_path']), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # -------------------------------------------------------------------------------------
    # ------------------------ 5 CREATING INTERVALS FOR THE CUTTING -----------------------
    # If videogrep failed (files with no sound also makes it return 1)
    if result == 1:
        increment_steps(mongo, metadata, 'Problem in conversion (probably video with no sound)')
    else:
        increment_steps(mongo, metadata, 'Finished..')
    return metadata


def silence_detection(path):
    """ Suppa fast silence detection"""
    frame_rate, data = scipy.io.wavfile.read(path)
    n_frames = len(data)
    duration_seconds = n_frames / frame_rate
    # print("number of frames: " + str(n_frames))
    # print("frame rate: " + str(frame_rate))
    # print("duration in seconds(n_frames/frame_rate):" + str(duration_seconds))
    silent_array = np.empty(int(duration_seconds))
    for second in range(int(duration_seconds)):
        is_second_silent = True
        # we don't really need to check each frame of the wave
        # in here we check every 20th frame
        for frame in range(int(frame_rate / 20)):
            if not is_silence(data[frame_rate * second + int(frame * 20)]):
                is_second_silent = False
        silent_array[second] = is_second_silent
    # note because we floor the duration of the video we skip a few frames of the last second
    # plt.plot(silent_array)
    # plt.show()
    return silent_array


# a function that tells us if this frame as silent or not. -> input [x,y]
def is_silence(frame, threshold=800):
    return threshold > abs(frame[0]) and threshold > abs(frame[1])


# returns [[t1, t2], [t3, t4]] for the time intervals of noise
def get_noise_interval(silence_array):
    time_array = []
    array_size = len(silence_array)
    i = 0
    while i < array_size:
        if silence_array[i] == 0:
            interval_of_time = 0
            t1 = i
            while i + interval_of_time < array_size and silence_array[i + interval_of_time] == 0:
                interval_of_time += 1
            t2 = t1 + interval_of_time
            i = i + interval_of_time
            time_array.append([t1, t2])
        i += 1
    # print(time_array)
    # print(list(enumerate(silence_array)))
    return time_array


# This function writes a srt subtitle file for videogrep
def write_noise_srt(noise_intervals, path):
    # remove the extension of a file by .srt (subtitle format)
    output_srt = os.path.splitext(path)[0] + '.srt'
    subs = []
    with open(output_srt, "w") as srt_file:
        i = 0
        while i < len(noise_intervals):
            noise_interval = "{}".format(i + 1) + "\n" \
                           + time.strftime('%H:%M:%S', time.gmtime(noise_intervals[i][0])) \
                           + ",000 --> " + time.strftime('%H:%M:%S', time.gmtime(noise_intervals[i][1])) \
                           + ",000\nNOISE\n\n"
            srt_file.write(noise_interval)
            subs.append(noise_interval)
            i += 1
    return subs

# ------- mongo stuff -------


def increment_steps(mongo, metadata, current_state=None):
    metadata['stepsCompleted'] += 1
    if current_state is not None:
        metadata['current_state'] = current_state
    mongo.db.metadata.update_one({'_id': metadata['_id']}, {"$set": metadata}, upsert=True)


def update_progress(mongo, metadata):
    mongo.db.metadata.update_one({'_id': metadata['_id']}, {"$set": metadata}, upsert=True)


# ignore this main, used this for testing while i was coding
if __name__ == '__main__':
    # silence_detection('/home/narsil/Documents/video-service/tmp/5b1c64140a234714d847df9b'
    #                  '.Wildlife_Windows_7_Sample_Video.mp4.wav')
    s_array = silence_detection('/home/narsil/Documents/video-service/tmp/5b1c834d0a23473183c321e4'
                                '.The_D_I_A_Take_Away_Show.mp4.wav')
    n_intervals = get_noise_interval(s_array)
    write_noise_srt(n_intervals, '/home/narsil/Documents/video-service/tmp/5b1c834d0a23473183c321e4'
                                 '.The_D_I_A_Take_Away_Show.mp4')
    # videogrep('/home/narsil/Documents/video-service/tmp/5b1c834d0a23473183c321e4'
    #           '.The_D_I_A_Take_Away_Show.mp4', '/home/narsil/Documents/video-service/tmp/CONVERTED.mp4', 'NOISE',
    #           're')
    # print(os.path.splitext(os.path.splitext(some_path)[0])[0])
