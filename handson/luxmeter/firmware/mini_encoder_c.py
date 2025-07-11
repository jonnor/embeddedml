# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# For M5Stack Hat Mini EncoderC, for M5StickC deices
# Ref https://docs.m5stack.com/en/hat/MiniEncoderC%20Hat
# Copied from https://github.com/m5stack/uiflow-micropython/blob/master/m5stack/libs/hat/mini_encoder_c.py

import struct


class MiniEncoderCHat:
    _ENCODER_COUNTER_VALUE_REG = 0x00
    _ENCODER_INCREMENT_VALUE_REG = 0x10
    _ENCODER_BUTTON_STATUS_REG = 0x20
    _ENCODER_RGB_LED_REG = 0x30
    _ENCODER_RESET_REG = 0x40
    _ENCODER_FIRMWARE_VERSION_REG = 0xFE
    _ENCODER_I2C_ADDRESS_REG = 0xFF

    def __init__(self, i2c, address: int | list | tuple = 0x42) -> None:
        self._i2c = i2c
        self._address = address
        self._buffer = memoryview(bytearray(5))
        if self._address not in self._i2c.scan():
            raise Exception("MiniEncoderC Hat maybe not connect")
        self._last_value = self._get_rotary_value()

    def get_rotary_status(self):
        val = self._get_rotary_value()
        if val != self._last_value:
            return True
        return False

    def get_rotary_value(self):
        self._last_value = self._get_rotary_value()
        return self._last_value

    def _get_rotary_value(self):
        buf = self._read_reg_bytes(self._ENCODER_COUNTER_VALUE_REG, 4)
        return struct.unpack("<i", buf)[0]

    def get_rotary_increments(self):
        buf = self._read_reg_bytes(self._ENCODER_INCREMENT_VALUE_REG, 4)
        return struct.unpack("<i", buf)[0]

    def reset_rotary_value(self):
        self._write_reg_bytes(self._ENCODER_RESET_REG, b"\x01")
        self._last_value = 0

    def set_rotary_value(self, val):
        self._last_value = val
        buf = self._buffer[1:5]
        struct.pack_into("<i", buf, 0, val)
        self._write_reg_bytes(self._ENCODER_RGB_LED_REG, buf)

    def get_button_status(self) -> bool:
        buf = self._read_reg_bytes(self._ENCODER_BUTTON_STATUS_REG, 2)
        return not bool(buf[0])

    def fill_color(self, rgb: int = 0) -> None:
        buf = self._buffer[1:4]
        buf[:] = rgb.to_bytes(3, "big")
        self._write_reg_bytes(self._ENCODER_RGB_LED_REG, buf)

    def read_fw_version(self) -> int:
        return self._read_reg_bytes(self._ENCODER_FIRMWARE_VERSION_REG)[0]

    def set_address(self, address: int) -> None:
        self._write_reg_bytes(self._ENCODER_I2C_ADDRESS_REG, address & 0xFF)
        self._address = address

    def _read_reg_bytes(self, reg: int = 0, len: int = 0) -> bytearray:
        buf = self._buffer[0:1]
        buf[0] = reg
        self._i2c.writeto(self._address, buf)
        buf = self._buffer[0:len]
        self._i2c.readfrom_into(self._address, buf)
        return buf

    def _write_reg_bytes(self, reg, data):
        buf = self._buffer[0 : 1 + len(data)]
        buf[0] = reg
        buf[1:] = bytes(data)
        self._i2c.writeto(self._address, buf)
