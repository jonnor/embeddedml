
from display import OledDisplay
from PIL import Image, ImageDraw
import numpy as np
import time

from pydantic import Field
from pydantic_settings import BaseSettings, CliApp, SettingsConfigDict



#import requests
#from prometheus_client.parser import text_string_to_metric_families


WIDTH, HEIGHT = 128, 64

def render_frame(cpu_pct: float, mem_pct: float, hostname: str) -> np.ndarray:
    img = Image.new("1", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(img)

    draw.text((0, 0), hostname, fill=1)
    draw.text((0, 12), f"CPU: {cpu_pct:5.1f}%", fill=1)
    draw.text((0, 22), f"MEM: {mem_pct:5.1f}%", fill=1)

    bar_x, bar_w, bar_h = 70, 50, 8
    draw.rectangle([bar_x, 12, bar_x + bar_w, 12 + bar_h], outline=1, fill=0)
    draw.rectangle([bar_x, 12, bar_x + int(bar_w * cpu_pct / 100), 12 + bar_h], fill=1)

    draw.rectangle([bar_x, 22, bar_x + bar_w, 22 + bar_h], outline=1, fill=0)
    draw.rectangle([bar_x, 22, bar_x + int(bar_w * mem_pct / 100), 22 + bar_h], fill=1)

    draw.line([0, 40, WIDTH - 1, 40], fill=1)
    draw.text((0, 48), "uptime: 3d 4h", fill=1)

    return np.array(img, dtype=np.uint8)

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="OLED_",
        cli_parse_args=True,
    )

    metrics_url: str = Field(
        default="http://localhost:9090/metrics",
        description="Prometheus metrics endpoint to scrape",
    )
    serial_port: str = Field(
        default="/dev/ttyACM0",
        description="Serial device path for the OLED display",
    )
    scl_pin: int = Field(default=17, description="I2C SCL pin")
    sda_pin: int = Field(default=18, description="I2C SDA pin")

def main():
    config = CliApp.run(Config)


    #resp = requests.get(config.metrics_url)
    #for family in text_string_to_metric_families(resp.text):
    #    for sample in family.samples:
    #        print(sample.name, sample.labels, sample.value)


    with OledDisplay(config.serial_port,
        scl_pin=config.scl_pin,
        sda_pin=config.sda_pin) as link:

        for i in range(50):
            frame = render_frame(
                cpu_pct=40 + 20 * (i % 10) / 10,
                mem_pct=60,
                hostname="myserver",
            )
            t0 = time.perf_counter()
            link.send_frame(frame)
            elapsed = time.perf_counter() - t0
            print(f"frame {i}: {elapsed*1000:.1f} ms")
            time.sleep(0.1)


if __name__ == "__main__":
    main()

