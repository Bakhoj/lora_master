import spidev
import time
import sys

# for a C++ example use below link:
# http://wiki.dragino.com/index.php?title=Use_Lora/GPS_HAT_%2B_RaspberryPi_to_set_up_a_Lora_Node
# maybe should change it to code in C++ instead since all the examples are in C++.
# https://www.hackster.io/idreams/getting-started-with-lora-fd69d1 

spi = spidev.SpiDev()
spi.open(0, 0)
#spi.max_speed_hz = 7629

def buildReadCommand(channel):
	startBit = 0x01
	singleEnded = 0x08

	return []

def processAdcValue(result):
	pass

def readAdc(channel):
	if ((channel > 7) or (channel < 0)):
		return -1

	r = spi.xfer(buildReadCommand(channel))
	return processAdcValue(r)

if __name__ == '__main__':
	try:
		while True:
			val = readAdc(0)
			print ("ADC Result: ", str(val))
			time.sleep(5)
	except KeyboardInterrupt as err:
		spi.close()
		sys.exit(0)


