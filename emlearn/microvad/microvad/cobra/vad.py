
# Based on example code from https://github.com/Picovoice/cobra/blob/main/demo/python/cobra_demo_file.py
# Copyright 2021 Picovoice Inc.
# License: Apache 2.0

import time
import argparse
import os

import soundfile
import pvcobra
import pandas


def read_file(file_name, sample_rate):

    audio, sr = soundfile.read(file_name, dtype='int16')
    assert sr == sample_rate   
    return audio

def predict_file(file_path, access_key=None, library_path=None, **kwargs):

    if access_key is None:
        access_key = os.envion['COBRA_ACCESS_KEY']

    cobra = pvcobra.create(library_path=library_path, access_key=access_key)

    audio = read_file(file_path, cobra.sample_rate)

    df = predict_audio(cobra, audio, **kwargs)

    cobra.delete()
    return df

def predict_audio(cobra, audio, threshold=0.5):

    start_time = time.time()

    times = []
    predictions = []
    num_frames = len(audio) // cobra.frame_length
    for i in range(num_frames):
        frame = audio[i * cobra.frame_length:(i + 1) * cobra.frame_length]
        result = cobra.process(frame)
        t = float(i * cobra.frame_length) / float(cobra.sample_rate)
        if result >= threshold:
            print("Detected voice activity at %0.1f sec" % t)
        times.append(t)
        predictions.append(result)

    end_time = time.time()

    df = pandas.DataFrame({
        'time': times,
        'probability': predictions,
    }).set_index('time')

    processing_time_ms = (end_time - start_time) * 1000.0
    print(f'Processing time {processing_time_ms} ms')

    return df

def parse():
    parser = argparse.ArgumentParser(description="Run PicoVoice Cobra VAD")

    parser.add_argument('input', help='Absolute path to input audio file.')

    parser.add_argument('--library_path', help='Absolute path to dynamic library.', default=pvcobra.LIBRARY_PATH)

    parser.add_argument('--access_key',
                        help='AccessKey provided by Picovoice Console (https://console.picovoice.ai/)',
                        required=True)

    parser.add_argument('--threshold', help="Threshold for the probability of voice activity",
                        type=float,
                        default=0.8)

    parser.add_argument('--out', help="Output file",
                        type=str,
                        default=None)

    args = parser.parse_args()
    return args

def main():
    args = parse()

    predictions = predict_file(args.input,
        threshold=args.threshold,
        access_key=args.access_key,
        library_path=args.library_path)

    predictions.to_csv(args.out)

if __name__ == '__main__':
    main()
