# Based on https://github.com/miketeachman/micropython-i2s-examples/blob/master/examples/record_mic_to_sdcard_blocking.py
# The MIT License (MIT)
# Copyright (c) 2022 Mike Teachman
# https://opensource.org/licenses/MIT

import os
from machine import Pin
from machine import I2S

SCK_PIN = 39
#WS_PIN = 25
SD_PIN = 38
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 40000

# ======= AUDIO CONFIGURATION =======
WAV_FILE = "mic.wav"
RECORD_TIME_IN_SECONDS = 4
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO
SAMPLE_RATE_IN_HZ = 16000
# ======= AUDIO CONFIGURATION =======

format_to_channels = {I2S.MONO: 1, I2S.STEREO: 2}
NUM_CHANNELS = format_to_channels[FORMAT]
WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
RECORDING_SIZE_IN_BYTES = (
    RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS
)


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


audio_in = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    #ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.PDM_RX,
    bits=WAV_SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ*2,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)

# allocate sample arrays
# memoryview used to reduce heap allocation in while loop
mic_samples = bytearray(10000)
mic_samples_mv = memoryview(mic_samples)


recording_buffer = bytearray(RECORDING_SIZE_IN_BYTES)
bytes_received = 0

print("Recording size: {} bytes".format(RECORDING_SIZE_IN_BYTES))
print("==========  START RECORDING ==========")
try:
    while bytes_received < RECORDING_SIZE_IN_BYTES:
        # read a block of samples from the I2S microphone
        bytes_read = audio_in.readinto(mic_samples_mv)
        if bytes_read > 0:
            bytes_to_write = min(
                bytes_read, RECORDING_SIZE_IN_BYTES - bytes_received
            )
            recording_buffer[bytes_received:bytes_received+bytes_to_write] = mic_samples_mv[0:bytes_to_write]
            print('FILL', bytes_received, bytes_to_write)
            bytes_received += bytes_read

    print("==========  DONE RECORDING ==========")
except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))


# Write to WAV
wav = open(WAV_FILE, "wb")

# create header for WAV file and write to SD card
wav_header = create_wav_header(
    SAMPLE_RATE_IN_HZ,
    WAV_SAMPLE_SIZE_IN_BITS,
    NUM_CHANNELS,
    SAMPLE_RATE_IN_HZ * RECORD_TIME_IN_SECONDS,
)
wav.write(wav_header)

# write samples to WAV file
wav.write(recording_buffer)

# cleanup
wav.close()
print("Wrote ", WAV_FILE)
audio_in.deinit()

