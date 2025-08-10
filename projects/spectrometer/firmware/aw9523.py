"""
aw9523.py

Basic LED drive-only driver for Adafruit's AW9523.
Written for micropython, no dependencies.
Largely inspired from Adafruit's library, which is based on CircuitPython
"""

__author__ = "Corentin J. Lapeyre"
__email__ = "corentin.lapeyre@gmail.com"
__version__ = "0.1.0"

_AW9523_DEFAULT_ADDR   = const(0x58)
_AW9523_REG_CHIPID     = const(0x10)  # Register for hardcode chip ID
_AW9523_REG_SOFTRESET  = const(0x7F)  # Register for soft resetting
_AW9523_REG_INTENABLE0 = const(0x06)  # Register for enabling interrupt
_AW9523_REG_GCR        = const(0x11)  # Register for general configuration
_AW9523_REG_LEDMODE    = const(0x12)  # Register for configuring const current
_AW9523_REG_CONFIG0 = const(0x04)
_AW9523_REG_CONFIG1 = const(0x05) 

class AW9523:
    """Basic LED driver for Adafruit's AW9523
    
    WARNING: only LED Driver mode (with 256 levels).
    No GPIO functionality.
    """

    _pin_to_addr = ([0x24 + pin for pin in range(7)] +
                    [0x20 + pin - 8 for pin in range(8, 12)] +
                    [0x2C + pin - 12 for pin in range(12, 16)])

    def __init__(self, i2c_bus, address=_AW9523_DEFAULT_ADDR):
        self.i2c_bus = i2c_bus
        self.address = address
        if (list(self.i2c_bus.readfrom_mem(address, _AW9523_REG_CHIPID, 1)) !=
            [0x23]):
            raise AttributeError("Cannot find a AW9523")
        self.reset()

    def _write(self, addr, *vals):
        self.i2c_bus.writeto_mem(self.address, addr, bytearray(list(vals)))

    def reset(self):
        """Perform a soft reset, check datasheets for post-reset defaults!"""
        self._write(_AW9523_REG_SOFTRESET, 0)
        self._write(_AW9523_REG_GCR, 0b00010000)  # pushpull output
        self._write(_AW9523_REG_INTENABLE0, 0xff, 0xff)  # no IRQ
        self._write(_AW9523_REG_LEDMODE, 0x00, 0x00)
        self._write(_AW9523_REG_CONFIG0, 0xFF, 0xFF) # direction, all out


    
    def __setitem__(self, idx, val):
        addrs = self._pin_to_addr[idx]
        if type(addrs) == int: addrs = [addrs]
        if type(val) == int: val = [val] * len(addrs)
        if not all([0 <= v <= 255 for v in val]):
            raise ValueError("Value must be 0 to 255")
        for a, v in zip(addrs, val):
            self._write(a, v)
