import io
import time
import uos
import asyncio
import microdot
from microdot import Microdot, Response  # noqa: F401

app = Microdot()

# Try to import WiFi credentials
try:
    from secrets import SSID, PASSWORD

    WIFI_AVAILABLE = True
    print("WiFi credentials loaded")
except ImportError:
    WIFI_AVAILABLE = False
    print("WiFi credentials not found, running in AP mode")

TEST_DATA_SIZE = 128 * 4096
TEST_DATA = bytes(TEST_DATA_SIZE)
print(f"Test data size: {TEST_DATA_SIZE} bytes")


@app.route("/")
def index(request):
    return "Hello from MicroPython webserver!"


@app.route("/status")
def status(request):
    import json

    status_data = {"status": "online", "firmware": "1.0.0"}
    return json.dumps(status_data), 200, {"Content-Type": "application/json"}


def generate_chunks(chunk_size):
    offset = 0
    data = memoryview(TEST_DATA)
    while offset < TEST_DATA_SIZE:
        end = offset + chunk_size
        if end > TEST_DATA_SIZE:
            end = TEST_DATA_SIZE
        yield data[offset:end]
        offset = end


@app.route("/stream")
def stream_data(request):
    chunk_size = int(request.args.get("chunk", 1024))

    headers = {
        "Content-Type": "application/octet-stream",
        "X-Total-Size": str(TEST_DATA_SIZE),
        "X-Chunk-Size": str(chunk_size),
    }

    return Response(
        body=generate_chunks(chunk_size),
        status_code=200,
        headers=headers,
    )


def generate_file_stream(filename, chunk_size):

    data = bytearray(chunk_size)
    with open(filename, "rb") as f:
        while True:
            n_read = f.readinto(data)
            if not n_read:
                break
            # FIXME: need memoryview to not send too much
            yield data


@app.route("/file-stream")
def file_stream_data(request):
    filename = request.args.get("file", "test.bin")
    chunk_size = int(request.args.get("chunk", 1024))

    try:
        file_size = uos.stat(filename)[6]
    except OSError:
        return f"File not found: {filename}", 404

    headers = {
        "Content-Type": "application/octet-stream",
        "X-Total-Size": str(file_size),
        "X-Chunk-Size": str(chunk_size),
    }

    return Response(
        body=generate_file_stream(filename, chunk_size),
        status_code=200,
        headers=headers,
    )


@app.route("/<endpoint>")
def endpoint(request, endpoint):
    text = "Request to: " + endpoint
    return text


async def logger_task():
    counter = 0
    while True:
        counter += 1
        print("Logger tick #" + str(counter))
        try:
            await asyncio.sleep(1)
        except:
            pass


async def main():
    import network
    import time

    logger = asyncio.create_task(logger_task())

    # Scan for WiFi networks
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    print("Scanning for WiFi networks...")
    ap_list = sta.scan()
    print(f"Found {len(ap_list)} networks:")
    for ap in ap_list:
        print(f"  SSID: {ap[0]}, RSSI: {ap[3]}, Auth: {ap[5]}")

    # Try to connect to configured network
    connected = False
    if WIFI_AVAILABLE:
        print(f"Trying to connect to {SSID}...")
        if not sta.isconnected():
            sta.connect(SSID, PASSWORD)
            for i in range(30):
                await asyncio.sleep(0.5)
                if sta.isconnected():
                    connected = True
                    print(f"Connected! IP: {sta.ifconfig()[0]}")
                    break
            if not connected:
                print("Failed to connect to WiFi")

    # Create test data file
    try:
        with open("test.bin", "wb") as f:
            f.write(TEST_DATA)
        print(f"Created test.bin ({TEST_DATA_SIZE} bytes)")
    except OSError as e:
        print(f"Failed to create test.bin: {e}")

    await app.start_server(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    asyncio.run(main())
