
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

class FrameRenderer():

    def __init__(self, token_generation_max=1000, token_read_rate_max=3000):
        # avoid font loading on every frame
        self.font_tiny = ImageFont.truetype("DejaVuSansMono.ttf", 10)
        self.font_small = ImageFont.truetype("DejaVuSansMono.ttf", 12)
        self.width = 128
        self.height = 64
        self.token_generation_max = token_generation_max
        self.token_read_rate_max = token_read_rate_max

    def render_bar(self, draw, value : float, x=0, y=0, width=None, height=10):
        if width is None:
            width = self.width

        # outline
        draw.rectangle([x, y, x + width, y + height], outline=1, fill=0)

        # bar
        draw.rectangle([x, y, x + int(width * value), y + height], fill=1)


    def render_frame(self, token_generation_rate: float,
            token_read_rate : float,    
            model: str,
            concurrent_requests: int) -> np.ndarray:

        tps = token_generation_rate
        width, height = self.width, self.height

        img = Image.new("1", (width, height), 0)
        draw = ImageDraw.Draw(img)

        # Show model name
        draw.text((0, 0), model, fill=1, font=self.font_tiny)
        line_y = 12
        draw.line([0, line_y, width - 1, line_y], fill=1)

        # Show tokens generated
        draw.text((0, 14), f"Gen: {token_generation_rate:6.0f} tok/s", fill=1, font=self.font_small)
        gen_scaled = (token_generation_rate / self.token_generation_max)
        self.render_bar(draw, value=gen_scaled, y=28, height=8)

        # read
        draw.text((0, 40), f"Read: {token_read_rate:5.0f} tok/s", fill=1, font=self.font_small)
        read_scaled = (token_read_rate / self.token_read_rate_max)
        self.render_bar(draw, value=read_scaled, y=52, height=8)

        # concurrency
        #y = 40
        #draw.text((0, y), f"Streams: {concurrent_requests:6.0f}", fill=1, font=self.font_small)

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

    meter_time_constant: float = 1.0

    log_interval_frame: int = 5


def fetch_metrics(metrics_url):

    if metrics_url.startswith('http'):
        data = requests.get(metrics_url).text

    else:
        # Supports loading from a local file. For test/development
        with open(metrics_url) as f:
            data = f.read()

    tokens_generated = None
    num_requests_running = None

    # Parse Prometheus
    metrics = {}
    for family in text_string_to_metric_families(data):
        for sample in family.samples:
            # NOTE: ignores sample.labels
            metrics[sample.name] = sample.value

    concurrent_requests = int(metrics['vllm:num_requests_running']) + \
        int(metrics['vllm:num_requests_waiting'])

    prompt_tokens_total = int(metrics['vllm:prompt_tokens_total'])

    tokens_generated = int(metrics['vllm:generation_tokens_total'])

    return tokens_generated, prompt_tokens_total, concurrent_requests

    
def main():
    config = CliApp.run(Config)

    gen_meter = RateMeter(time_constant=config.meter_time_constant)
    read_meter = RateMeter(time_constant=config.meter_time_constant)
    renderer = FrameRenderer(token_generation_max=500)
    frame_log_interval = config.log_interval_frame

    with OledDisplay(config.serial_port,
        scl_pin=config.scl_pin,
        sda_pin=config.sda_pin) as link:

        frame_no = 0
        while True:
            t0 = time.perf_counter()

            total_tokens_generated, prompt_tokens_total, concurrent_requests = \
                fetch_metrics(config.metrics_url)

            token_generation_rate = gen_meter.update(total_tokens_generated)
            token_read_rate = read_meter.update(prompt_tokens_total)

            if token_generation_rate is not None:
                frame = renderer.render_frame(
                    model="Qwen-3.8-27B (vLLM)",
                    token_generation_rate=token_generation_rate,
                    token_read_rate=token_read_rate,
                    concurrent_requests=concurrent_requests,
                )
                link.send_frame(frame)

            elapsed = time.perf_counter() - t0

            if (frame_no % frame_log_interval) == 0:

                logger.info('frame',
                    i=frame_no,
                    token_generation_rate=None if token_generation_rate is None else round(token_generation_rate, 1),
                    token_read_rate=None if token_read_rate is None else round(token_read_rate, 1),
                    total_tokens_generated=total_tokens_generated,
                    prompt_tokens_total=prompt_tokens_total,
                    duration=round(elapsed, 3),
                )

            time.sleep(0.250)
            frame_no += 1


if __name__ == "__main__":
    main()

