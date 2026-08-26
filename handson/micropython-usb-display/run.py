#!/usr/bin/env python3
"""
Benchmark: send a base64-encoded 128x64 SSD1306 frame via mpremote's raw REPL
and time round-trip latency for exec() + decode + blit + show.

Usage: python3 bench.py /dev/ttyUSB0
"""
import sys
import time
import base64
import random
from mpremote.transport_serial import SerialTransport

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
N_FRAMES = 100
FRAME_SIZE = 1024  # 128*64/8

def random_frame():
    return bytes(random.getrandbits(8) for _ in range(FRAME_SIZE))

def main():
    print(f"Connecting to {PORT}...")
    t = SerialTransport(PORT)
    t.enter_raw_repl()

    setup_code = """
import ssd1306, ubinascii
from machine import Pin, I2C
if 'oled' not in globals():
    i2c = I2C(0, scl=Pin(17), sda=Pin(18), freq=400000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
"""
    t.exec(setup_code)
    print("Remote setup done. Starting benchmark...")

    latencies = []
    for i in range(N_FRAMES):
        frame = random_frame()
        b64 = base64.b64encode(frame).decode()

        cmd = f"oled.buffer[:] = ubinascii.a2b_base64({b64!r}); oled.show()"

        t0 = time.perf_counter()
        t.exec(cmd)
        t1 = time.perf_counter()

        latencies.append(t1 - t0)
        print(f"frame {i:3d}: {(t1 - t0) * 1000:.1f} ms")

    t.exit_raw_repl()
    t.close()

    latencies.sort()
    n = len(latencies)
    avg = sum(latencies) / n
    p50 = latencies[n // 2]
    p95 = latencies[int(n * 0.95)]
    worst = latencies[-1]
    best = latencies[0]

    print("\n--- Results ---")
    print(f"frames:      {n}")
    print(f"best:        {best*1000:.1f} ms")
    print(f"avg:         {avg*1000:.1f} ms  ({1/avg:.1f} Hz)")
    print(f"median:      {p50*1000:.1f} ms  ({1/p50:.1f} Hz)")
    print(f"p95:         {p95*1000:.1f} ms  ({1/p95:.1f} Hz)")
    print(f"worst:       {worst*1000:.1f} ms")

if __name__ == "__main__":
    main()
