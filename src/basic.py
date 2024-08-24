#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick PoC for interrogating the pH/ORP sensor
"""

import structlog
import minimalmodbus

log = structlog.get_logger(__name__)

# Change as needed
PORT = "/dev/ttyUSB0"
# Defaults from the datasheet: _docs/pH_EC Sensor.pdf
BAUDRATE = 9600
SENSOR_ADDR = 0x01
PH_REGISTER = 0x00
ORP_REGISTER = 0x01


def main():
    """Does the needful"""
    log.error("Starting basic.py")
    instrument = minimalmodbus.Instrument(PORT, SENSOR_ADDR, debug=True)

    if instrument.serial is None:
        log.error("Serial is None")
        return

    instrument.serial.baudrate = BAUDRATE
    instrument.serial.timeout = 1

    instrument.clear_buffers_before_each_transaction = True

    # read_register() does the decode/parse for us but using the raw bytes is more illustrative.
    # The datasheet tells us that both measurements are 16 bits and gives an example
    # payload of 0x02, 0xAE, 0x01, 0x94. This is 0x02AE = 686, 0x0194 = 404.
    # And the datasheet says that the PH value is 6.86 and the ORP value is 404.
    #
    # 0x01 0x94 = 1 * 256 + 148 = 404
    # 0x02 0xAE = 2 * 256 + 174 = 686
    # And then just insert the decimal point at the right place.
    ##
    ph = instrument.read_register(PH_REGISTER, number_of_decimals=2, signed=True)
    orp = instrument.read_register(ORP_REGISTER, number_of_decimals=0, signed=True)

    log.info("Readings:", pH=ph, orp=orp)


if __name__ == "__main__":
    main()
