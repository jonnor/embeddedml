
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

recording_time = 3.0
# ======= AUDIO CONFIGURATION =======

RECORD = 0
PAUSE = 1
RESUME = 2
STOP = 3

format_to_channels = {I2S.MONO: 1, I2S.STEREO: 2}
NUM_CHANNELS = format_to_channels[FORMAT]
WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
RECORDING_SIZE_BYTES = int(recording_time*SAMPLE_RATE_IN_HZ*WAV_SAMPLE_SIZE_IN_BYTES)

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
    global bytes_received
    global mic_samples_mv
    global num_read

    if state == RECORD:
        bytes_read = num_read
        bytes_to_write = min(bytes_read, RECORDING_SIZE_BYTES - bytes_received)
        recording_buffer[bytes_received:bytes_received+bytes_to_write] = mic_samples_mv[0:bytes_to_write]
        bytes_received += bytes_to_write
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

        # write data to wav file
        wav = open(WAV_FILE, "wb")

        # create header for WAV file and write to SD card
        wav_header = create_wav_header(
            SAMPLE_RATE_IN_HZ,
            WAV_SAMPLE_SIZE_IN_BITS,
            NUM_CHANNELS,
            len(recording_buffer) // (WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS),
        )

        wav.write(wav_header)
        wav.write(recording_buffer)
        
        # cleanup
        wav.close()
        audio_in.deinit()
        print("Done")
    else:
        print("Not a valid state.  State ignored")



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

recording_buffer = bytearray(RECORDING_SIZE_BYTES)
bytes_received = 0

state = PAUSE
# start the background activity to read the microphone.
# the callback will keep the activity continually running in the background.
num_read = audio_in.readinto(mic_samples_mv)

# === Main program code goes here ===
# audio sample recording to SD card will be running in the background
# changing 'state' can cause the recording to Pause, Resume, or Stop

def fibonacci_iterative(n):
  a, b = 0, 1
  for i in range(n):
    a, b = b, a + b
  return a

print("starting recording for", recording_time)
state = RECORD

start = time.ticks_ms()
while True:
    dt = time.ticks_diff(time.ticks_ms(), start) / 1000.0

    # simulate some work being done
    processing_start = time.ticks_us()
    fibonacci_iterative(n=1000)
    processing = time.ticks_diff(time.ticks_us(), processing_start) / 1000.0 # ms
    print('PROCESS t=', dt, 'processing=', processing, '(ms)')
    
    # wait until next main loop iter
    time.sleep_ms(100)

    if dt > recording_time:
        print("stopping recording and closing WAV file")
        state = STOP
        break