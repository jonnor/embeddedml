import asyncio
from microdot import Microdot, Response

app = Microdot()

test_data = b'X' * 10240

@app.route("/test")
def test(request):
    return test_data

@app.route("/stream")
async def stream(request):
    async def gen():
        yield test_data[:5120]
        yield test_data[5120:]
    return Response(body=gen(), status_code=200)

if __name__ == "__main__":
    asyncio.run(app.start_server(host="127.0.0.1", port=8000))
