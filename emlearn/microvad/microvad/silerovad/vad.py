
# TODO: support running C++ version
# https://github.com/snakers4/silero-vad/tree/master/examples/cpp

import time
from pprint import pprint

import torch
import numpy
import pandas


def get_frame_scores(audio: torch.Tensor,
                          model,
                          sampling_rate: int = 16000,
                          window_size_samples: int = 512):

    """
    Return frame-wise scores / probabilities

    Parameters
    ----------
    audio: torch.Tensor, one dimensional
        One dimensional float torch.Tensor, other types are casted to torch if possible

    model: preloaded .jit silero VAD model

    sampling_rate: int (default - 16000)
        Currently silero VAD models support 8000 and 16000 sample rates

    window_size_samples: int (default - 512 samples)
        Audio chunks of window_size_samples size are fed to the silero VAD model.
        WARNING! Silero VAD models were trained using 512, 1024, 1536 samples for 16000 sample rate
        and 256, 512, 768 samples for 8000 sample rate.
        Values other than these may affect model perfomance!!

    Returns
    ----------
    speeches: list of dicts
        list containing ends and beginnings of speech chunks (samples or seconds based on return_seconds)
    """

    if not torch.is_tensor(audio):
        try:
            audio = torch.Tensor(audio)
        except:
            raise TypeError("Audio cannot be casted to tensor. Cast it manually")

    if len(audio.shape) > 1:
        for i in range(len(audio.shape)):  # trying to squeeze empty dimensions
            audio = audio.squeeze(0)
        if len(audio.shape) > 1:
            raise ValueError("More than one dimension in audio. Are you trying to process audio with 2 channels?")

    if sampling_rate > 16000 and (sampling_rate % 16000 == 0):
        step = sampling_rate // 16000
        sampling_rate = 16000
        audio = audio[::step]
        warnings.warn('Sampling rate is a multiply of 16000, casting to 16000 manually!')
    else:
        step = 1

    if sampling_rate == 8000 and window_size_samples > 768:
        warnings.warn('window_size_samples is too big for 8000 sampling_rate! Better set window_size_samples to 256, 512 or 768 for 8000 sample rate!')
    if window_size_samples not in [256, 512, 768, 1024, 1536]:
        warnings.warn('Unusual window_size_samples! Supported window_size_samples:\n - [512, 1024, 1536] for 16000 sampling_rate\n - [256, 512, 768] for 8000 sampling_rate')

    model.reset_states()

    audio_length_samples = len(audio)

    speech_probs = []
    for current_start_sample in range(0, audio_length_samples, window_size_samples):
        chunk = audio[current_start_sample: current_start_sample + window_size_samples]
        if len(chunk) < window_size_samples:
            chunk = torch.nn.functional.pad(chunk, (0, int(window_size_samples - len(chunk))))
        speech_prob = model(chunk, sampling_rate).item()
        speech_probs.append(speech_prob)

    return speech_probs


def predict_file(model, path, samplerate = 16000, window_size_samples = 512):
    
    model, utils = model
    (get_speech_timestamps, _, read_audio, *_) = utils
   

    wav = read_audio(path, sampling_rate=samplerate)

    # Run model to get raw predictions / probabilities
    start_time = time.time()
    speech_probs = get_frame_scores(wav, model,
        sampling_rate=samplerate,
        window_size_samples=window_size_samples)
    end_time = time.time()

    predict_time_ms = (end_time-start_time) * 1000.0
    print(f'prediction time {predict_time_ms} ms')

    times = numpy.arange(0, len(speech_probs)) * window_size_samples/samplerate

    # get post-procesed speech segments
    #speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=samplerate, return_seconds=True)

    df = pandas.DataFrame({
        'time': times,
        'probability': speech_probs,
    })
    return df


def load_model(force_reload=False):
    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                  model='silero_vad',
                                  force_reload=force_reload)

    return (model, utils)


def parse(args=None):
    import argparse

    parser = argparse.ArgumentParser(description='Voice Activity Detection using Silero VAD')
    a = parser.add_argument

    a('input', type=str, metavar='PATH',
      help='Path to input audio file')

    a('--out', type=str, metavar='PATH', default=None,
      help='Path to output file. CSV')

    parsed = parser.parse_args(args)
    return parsed

def main():
    args = parse()

    torch.set_num_threads(1)

    m = load_model()

    probs = predict_file(m, args.input)
    out_path = args.out
    if out_path is not None:
        probs.to_csv(out_path)
        print('Wrote', out_path)

if __name__  == '__main__':
    main()
    


    
