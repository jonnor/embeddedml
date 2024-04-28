
import os
import time
from machine import Pin
from machine import I2S


SCK_PIN = 39
#WS_PIN = 25
SD_PIN = 38
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 80000

# ======= AUDIO CONFIGURATION =======
WAV_FILE = "mic.wav"
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO
SAMPLE_RATE_IN_HZ = 16000
# ======= AUDIO CONFIGURATION =======

RECORD = 0
PAUSE = 1
RESUME = 2
STOP = 3

format_to_channels = {I2S.MONO: 1, I2S.STEREO: 2}
NUM_CHANNELS = format_to_channels[FORMAT]
WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8


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


def i2s_callback_rx(arg):
    global state
    global num_sample_bytes_written_to_wav
    global mic_samples_mv
    global num_read

    if state == RECORD:
        num_bytes_written = wav.write(mic_samples_mv[:num_read])
        num_sample_bytes_written_to_wav += num_bytes_written
        # read samples from the I2S device.  This callback function
        # will be called after 'mic_samples_mv' has been completely filled
        # with audio samples
        num_read = audio_in.readinto(mic_samples_mv)
    elif state == RESUME:
        state = RECORD
        num_read = audio_in.readinto(mic_samples_mv)
    elif state == PAUSE:
        # in the PAUSE state read audio samples from the I2S device
        # but do not write the samples to SD card
        num_read = audio_in.readinto(mic_samples_mv)
    elif state == STOP:
        # create header for WAV file and write to SD card
        wav_header = create_wav_header(
            SAMPLE_RATE_IN_HZ,
            WAV_SAMPLE_SIZE_IN_BITS,
            NUM_CHANNELS,
            num_sample_bytes_written_to_wav // (WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS),
        )
        _ = wav.seek(0)  # advance to first byte of Header section in WAV file
        num_bytes_written = wav.write(wav_header)
        # cleanup
        wav.close()
        audio_in.deinit()
        print("Done")
    else:
        print("Not a valid state.  State ignored")


wav = open(WAV_FILE, "wb")
pos = wav.seek(44)  # advance to first byte of Data section in WAV file

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

# setting a callback function makes the
# readinto() method Non-Blocking
audio_in.irq(i2s_callback_rx)

# allocate sample arrays
# memoryview used to reduce heap allocation in while loop
mic_samples = bytearray(1000)
mic_samples_mv = memoryview(mic_samples)

num_sample_bytes_written_to_wav = 0

state = PAUSE
# start the background activity to read the microphone.
# the callback will keep the activity continually running in the background.
num_read = audio_in.readinto(mic_samples_mv)

# === Main program code goes here ===
# audio sample recording to SD card will be running in the background
# changing 'state' can cause the recording to Pause, Resume, or Stop

print("starting recording for 5s")
state = RECORD
time.sleep(5.0)
print("stopping recording and closing WAV file")
state = STOP
