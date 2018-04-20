import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 7629

def write_pot(input):
    msb = input >> 8
    lsb = input & 0xFF
    spi.xfer([msb, lsb])

while true:
    write_pot(0x1FF)
    time.sleep(0.5)
    write_pot(0x00)
    time.sleep(0.5)
    