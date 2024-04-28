
# Originally based on 
# https://github.com/miketeachman/micropython-i2s-examples/blob/master/examples/record_mic_to_sdcard_non_blocking.py
# but a near complete rewrite, to use a queue on the input

import os
import time
from machine import Pin
from machine import I2S


def create_wav_header(sampleRate, bitsPerSample, num_channels, num_samples):
    datasize = num_samples * num_channels * bitsPerSample // 8
    o = bytes("RIFF", "ascii")  # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(
        4, "little"
    )  # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE", "ascii")  # (4byte) File type
    o += bytes("fmt ", "ascii")  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, "little")  # (4byte) Length of above format data
    o += (1).to_bytes(2, "little")  # (2byte) Format type (1 - PCM)
    o += (num_channels).to_bytes(2, "little")  # (2byte)
    o += (sampleRate).to_bytes(4, "little")  # (4byte)
    o += (sampleRate * num_channels * bitsPerSample // 8).to_bytes(4, "little")  # (4byte)
    o += (num_channels * bitsPerSample // 8).to_bytes(2, "little")  # (2byte)
    o += (bitsPerSample).to_bytes(2, "little")  # (2byte)
    o += bytes("data", "ascii")  # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4, "little")  # (4byte) Data size in bytes
    return o

from collections import deque

class AudioInput():
    def __init__(self, i2s, buffers=4, chunk=10000):

        self.i2s = i2s
        self.chunk_size = chunk
        self.buffers = buffers

        # allocate sample arrays
        self.mic_samples = bytearray(chunk)
        self.mic_samples_mv = memoryview(self.mic_samples)

        self.queue = deque([], self.buffers)

        # setting a callback function makes the readinto() method Non-Blocking
        self.i2s.irq(self.i2s_callback_rx)

        read = self.i2s.readinto(self.mic_samples_mv)
        assert read == self.chunk_size
        
        self.overflows = 0
        
    def i2s_callback_rx(self, arg):
        # check for overflow
        if len(self.queue) == self.buffers:
            self.overflows += 1

        # queue incoming data
        data = self.mic_samples_mv[:self.chunk_size] # make copy
        self.queue.append(data)

        # trigger next
        read = self.i2s.readinto(self.mic_samples_mv)
        assert read == self.chunk_size
        #print('RX', read)

    def get(self):
        if len(self.queue) == 0:
            return None
        else:
            return self.queue.pop() 


class WavWriter():

    def __init__(self, samplerate, channels=1, bitdepth=16):
        # config
        self.samplerate = samplerate
        self.channels = 1
        self.bitdepth = bitdepth

        # state
        self.file = None
        self.bytes_written = 0
    
    def start(self, path):
        self.file = open(path, "wb")
        _ = self.file.seek(44)  # advance to first byte of Data section in WAV file

    def add(self, samples):
        # XXX: consumer is required to pass data in the correct sample format
        written = self.file.write(samples)
        self.bytes_written += written

    def stop(self):
    
        sample_size_bytes = self.bitdepth // 8
        samples = self.bytes_written // (sample_size_bytes * self.channels)

        # write the WAV header to start of file
        wav_header = create_wav_header(self.samplerate, self.bitdepth, self.channels, samples)
        _ = self.file.seek(0)  # advance to first byte of Header section in WAV file
        _ = self.file.write(wav_header)

        # reset state
        self.file.close()
        self.file = None
        self.bytes_written = 0

def main():

    FORMAT = I2S.MONO
    SAMPLERATE = 16000
    BITDEPTH = 32
    BUFFER_LENGTH = 40000

    # 38/39 is pins on M5Stack AtomS3U
    audio_in = I2S(0,
        sck=Pin(39),
        sd=Pin(38),
        mode=I2S.PDM_RX,
        ws=None, # unused for PDM
        bits=BITDEPTH,
        format=FORMAT,
        rate=SAMPLERATE,
        ibuf=BUFFER_LENGTH,
    )

    audio_input = AudioInput(audio_in, chunk=4000)

    WAV_FILE = "mic.wav"
    wav_writer = WavWriter(samplerate=SAMPLERATE, bitdepth=BITDEPTH//2)
    wav_writer.start(WAV_FILE)

    record_duration = 5.0
    start = time.ticks_ms()

    while True:
        dt = time.ticks_diff(time.ticks_ms(), start) / 1000.0
        # check for new input audio
        audio_chunk = audio_input.get()
        if audio_chunk and wav_writer.file:
            wav_writer.add(audio_chunk)
            print('wav-write', dt, wav_writer.bytes_written, audio_input.overflows)
        
        if len(audio_input.queue) == 4:
            raise Exception()
        
        if (dt > record_duration) and wav_writer.file:
            wav_writer.stop()
            print('waw-stop', dt)

        time.sleep_ms(10)

if __name__ == '__main__':
    main()

