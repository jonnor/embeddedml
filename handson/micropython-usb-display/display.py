
"""
oled_link.py — reusable class for pushing SSD1306 framebuffers to an
ESP32 (MicroPython) over mpremote's raw REPL.

Frames are passed as numpy arrays of shape (height, width), dtype bool
or uint8 (nonzero = lit pixel).
"""
import base64
import numpy as np
from mpremote.transport_serial import SerialTransport


class OledDisplay:
    """
    Drives a remote SSD1306 OLED over USB serial via MicroPython's raw REPL.

    Usage:
        link = OledLink("/dev/ttyUSB0", scl_pin=17, sda_pin=18)
        link.connect()
        link.send_frame(frame_array)   # numpy array, shape (64, 128)
        link.close()

    Or as a context manager:
        with OledLink("/dev/ttyUSB0", scl_pin=17, sda_pin=18) as link:
            link.send_frame(frame_array)
    """

    def __init__(
        self,
        port: str,
        scl_pin: int,
        sda_pin: int,
        width: int = 128,
        height: int = 64,
        i2c_id: int = 0,
        i2c_freq: int = 400_000,
        i2c_addr: int | None = None,
    ):
        self.port = port
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self.width = width
        self.height = height
        self.i2c_id = i2c_id
        self.i2c_freq = i2c_freq
        self.i2c_addr = i2c_addr  # None -> use driver default (0x3C)

        self.frame_size = (width * height) // 8
        self._transport: SerialTransport | None = None

    # -- lifecycle -----------------------------------------------------

    def connect(self) -> None:
        """Open the serial connection, enter raw REPL, and set up the OLED."""
        self._transport = SerialTransport(self.port)
        self._transport.enter_raw_repl()

        addr_arg = f", addr={self.i2c_addr}" if self.i2c_addr is not None else ""
        setup_code = f"""
import ssd1306, ubinascii
from machine import Pin, I2C
if 'oled' not in globals():
    i2c = I2C({self.i2c_id}, scl=Pin({self.scl_pin}), sda=Pin({self.sda_pin}), freq={self.i2c_freq})
    oled = ssd1306.SSD1306_I2C({self.width}, {self.height}, i2c{addr_arg})
"""
        self._transport.exec(setup_code)

    def close(self) -> None:
        """Exit raw REPL and close the serial connection."""
        if self._transport is not None:
            self._transport.exit_raw_repl()
            self._transport.close()
            self._transport = None

    def __enter__(self) -> "OledLink":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # -- conversion ------------------------------------------------------

    def _array_to_bytes(self, arr: np.ndarray) -> bytes:
        """Convert a (height, width) numpy array into SSD1306 page-ordered bytes."""
        if arr.shape != (self.height, self.width):
            raise ValueError(
                f"frame array must have shape ({self.height}, {self.width}), "
                f"got {arr.shape}"
            )

        bits = (arr != 0).astype(np.uint8)  # 0 or 1, shape (height, width)
        buf = bytearray(self.frame_size)
        n_pages = self.height // 8
        for page in range(n_pages):
            rows = bits[page * 8 : page * 8 + 8, :]  # (8, width)
            col_bytes = np.zeros(self.width, dtype=np.uint8)
            for bit in range(8):
                col_bytes |= (rows[bit, :] << bit).astype(np.uint8)
            buf[page * self.width : (page + 1) * self.width] = col_bytes.tobytes()
        return bytes(buf)

    # -- data path -------------------------------------------------------

    def send_frame(self, frame: np.ndarray) -> None:
        """
        Send a frame (numpy array, shape (height, width), nonzero = lit)
        to the display and call show().
        """
        if self._transport is None:
            raise RuntimeError("OledLink is not connected; call connect() first")

        frame_bytes = self._array_to_bytes(frame)
        b64 = base64.b64encode(frame_bytes).decode()
        cmd = f"oled.buffer[:] = ubinascii.a2b_base64({b64!r}); oled.show()"
        self._transport.exec(cmd)

    def clear(self) -> None:
        """Clear the display to all-black."""
        self.send_frame(np.zeros((self.height, self.width), dtype=np.uint8))
