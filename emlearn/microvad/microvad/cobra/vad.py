
# Based on example code from https://github.com/Picovoice/cobra/blob/main/demo/python/cobra_demo_file.py
# Copyright 2021 Picovoice Inc.
# License: Apache 2.0

import time
import argparse

import soundfile
import pvcobra


def read_file(file_name, sample_rate):

    audio, sr = soundfile.read(file_name, dtype='int16')
    assert sr == sample_rate
    
    return audio


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help='Absolute path to input audio file.')

    parser.add_argument('--library_path', help='Absolute path to dynamic library.', default=pvcobra.LIBRARY_PATH)

    parser.add_argument('--access_key',
                        help='AccessKey provided by Picovoice Console (https://console.picovoice.ai/)',
                        required=True)

    parser.add_argument('--threshold', help="Threshold for the probability of voice activity",
                        type=float,
                        default=0.8)

    args = parser.parse_args()

    cobra = pvcobra.create(library_path=args.library_path, access_key=args.access_key)
    print("Cobra version: %s" % cobra.version)
    audio = read_file(args.input, cobra.sample_rate)

    start_time = time.time()

    num_frames = len(audio) // cobra.frame_length
    for i in range(num_frames):
        frame = audio[i * cobra.frame_length:(i + 1) * cobra.frame_length]
        result = cobra.process(frame)
        if result >= args.threshold:
            print("Detected voice activity at %0.1f sec" % (float(i * cobra.frame_length) / float(cobra.sample_rate)))

    end_time = time.time()

    processing_time_ms = (end_time - start_time) * 1000.0
    print(f'Processing time {processing_time_ms} ms')

    cobra.delete()


if __name__ == '__main__':
    main()
