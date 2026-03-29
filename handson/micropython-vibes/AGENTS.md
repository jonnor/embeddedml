# MicroPython ESP32 Web Server - Learning Summary

## Project Goal
Deploy and test a MicroPython web server on ESP32 that streams data in configurable chunk sizes via HTTP endpoints.

## Project file structure
- `firmware/micropython/server.py` - Main server with streaming
- `firmware/micropython/microdot.py` - MicroPython-compatible microdot
- `firmware/micropython/secrets.py` - WiFi credentials
- `firmware/benchmark.py` - Performance testing
- Device files: `:/server.py`, `:/microdot.py`, `:/secrets.py`

## Key Learnings

### 0. MicroPython running on hardware device

- **Critical**: Do NOT put code in boot.py or main.py (for development safety)
- Upload: `mpremote cp firmware/micropython/server.py :/server.py`
- Run: `mpremote run firmware/micropython/server.py`
- Reset: `mpremote reset`

### 0. MicroPython libraries

- The following are standard Python libraries that are included by default with MicroPython: array, binascii, collections, errno, gzip, hashlib, heapq, io, json, os, platform, random, re, select, socket, ssl, struct, time, zlib, math, cmath, asyncio
They API of these moduels follow standard Python libraries. Always use the standard libraries with these names. Never use uos, uasyncio, etc.
- The following are MicroPython specific modules, that can be used on device only:
machine, micropython, bluetooth, network, gc

### 1. MicroPython running locally

- Can run programs under MicroPython on PC by using the `micropython` command-line tool.
It is important to use this for testing MicroPython code, instead of `python` command.

### 2. Memory Constraints
- ESP32 has very limited RAM compared to development machine
- 1MB test data causes allocation failure
- Need to keep data small and avoid unnecessary allocations

### 3. WiFi Connection Strategy
- User specified **station mode only** (STA_IF), not AP mode
- Need to scan for networks and attempt STA connection

### 4. Server Architecture
- Server runs as async task with background logger
- Streaming endpoint supports `?chunk=8192` query parameter
- Server holds serial connection while running - prevents mpremote commands

### 6. Development Workflow Issues
- **Serial Blocking**: When server runs, it blocks mpremote commands.
Try `mpremote reset` to get back control
- **File Transfer**: Use mpremote cp to copy files to device

### 7. MicroPython Import Structure
- MicroPython on ESP32 expects `microdot.py` as standalone module in filesystem
- Cannot import from subdirectories easily on ESP32
- All modules must be at root of filesystem

### 9. MicroPython Async Limitations
- **Issue**: MicroPython's `async def` generators don't work like CPython - they return regular generators, not async generators
- **Solution**: Convert async generator to sync generator by removing `async def` and `await asyncio.sleep(0)`
- This is a fundamental difference between MicroPython and CPython

