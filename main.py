import spidev
import time

# for a C++ example use below link:
# http://wiki.dragino.com/index.php?title=Use_Lora/GPS_HAT_%2B_RaspberryPi_to_set_up_a_Lora_Node
# maybe should change it to code in C++ instead since all the examples are in C++.
# https://www.hackster.io/idreams/getting-started-with-lora-fd69d1 

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
    