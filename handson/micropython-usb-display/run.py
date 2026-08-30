
from display import OledDisplay
from PIL import Image, ImageDraw
import numpy as np
import time

from pydantic import Field
from pydantic_settings import BaseSettings, CliApp, SettingsConfigDict

import requests
from prometheus_client.parser import text_string_to_metric_families


import math
import time
from typing import Optional

import structlog

logger = structlog.get_logger()


class RateMeter:
    """
    Tracks the rate of change of a monotonically increasing total,
    smoothed with first-order exponential smoothing (EMA), robust to
    irregular call intervals.
    """

    def __init__(self, time_constant: float = 5.0):
        self.time_constant = time_constant
        self._prev_total: Optional[float] = None
        self._prev_time: Optional[float] = None
        self._smoothed_rate: Optional[float] = None

    def update(self, total: float, now: Optional[float] = None) -> Optional[float]:
        if now is None:
            now = time.time()

        if self._prev_total is None:
            self._prev_total = total
            self._prev_time = now
            return None

        dt = now - self._prev_time
        if dt <= 0:
            logger.warning(
                "ratemeter_non_positive_dt",
                dt=dt,
                now=now,
                prev_time=self._prev_time,
            )
            return self._smoothed_rate

        instant_rate = (total - self._prev_total) / dt

        if self._smoothed_rate is None:
            self._smoothed_rate = instant_rate
        else:
            alpha = 1 - math.exp(-dt / self.time_constant)
            self._smoothed_rate += alpha * (instant_rate - self._smoothed_rate)

        self._prev_total = total
        self._prev_time = now
        return self._smoothed_rate

    @property
    def rate(self) -> Optional[float]:
        return self._smoothed_rate

    def reset(self):
        self._prev_total = None
        self._prev_time = None
        self._smoothed_rate = None

from PIL import Image, ImageDraw, ImageFont

def render_frame(cpu_pct: float, mem_pct: float, hostname: str, width=128, height=64) -> np.ndarray:

    font_tiny = ImageFont.truetype("DejaVuSansMono.ttf", 10)
    font_small = ImageFont.truetype("DejaVuSansMono.ttf", 12)


    img = Image.new("1", (width, height), 0)
    draw = ImageDraw.Draw(img)

    draw.text((0, 0), hostname, fill=1, font=font_tiny)
    draw.line([0, 12, width - 1, 10], fill=1)

    draw.text((0, 14), f"CPU: {cpu_pct:5.1f}%", fill=1, font=font_small)

    bar_x, bar_w, bar_h = 0, 100, 20
    bar_y = 28
    draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], outline=1, fill=0)
    draw.rectangle([bar_x, bar_y, bar_x + int(bar_w * cpu_pct / 100), bar_y + bar_h], fill=1)

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


    metrics_url = config.metrics_url
    if metrics_url.startswith('http'):
        data = requests.get(metrics_url).text

    else:
        with open(metrics_url) as f:
            data = f.read()

    value = None
    for family in text_string_to_metric_families(data):
        for sample in family.samples:
            if sample.name == 'vllm:generation_tokens_total':
                #print(sample.name, sample.labels, sample.value)
                value = sample.value

    meter = RateMeter(time_constant=1.0)

    print('value', value/10)
    meter.update(0) # start at 0
    time.sleep(0.1)


    with OledDisplay(config.serial_port,
        scl_pin=config.scl_pin,
        sda_pin=config.sda_pin) as link:

        for i in range(50):
            tps = meter.update(value/10)

            frame = render_frame(
                cpu_pct=tps,
                mem_pct=60,
                hostname="Qwen-3.8-27B (vLLM)",
            )
            t0 = time.perf_counter()
            link.send_frame(frame)
            elapsed = time.perf_counter() - t0
            print(f"frame {i}: {elapsed*1000:.1f} ms")
            time.sleep(0.1)


if __name__ == "__main__":
    main()

