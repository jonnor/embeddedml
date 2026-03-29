import microdot
from microdot import Microdot

app = Microdot()


@app.route("/")
def index(request):
    return "Hello from MicroPython!"


@app.route("/status")
def status(request):
    import json

    return json.dumps({"status": "online"}), 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    print("Starting server on 0.0.0.0:5000...")
    app.run(host="0.0.0.0", port=5000)
