import time
import sys
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from weather_master import PackageReader
from aws import AWS

print("Start Master Module")

BOARD.DIO0 = 4
BOARD.DIO3 = 1
#BOARD.DIO3 = 26
BOARD.SWITCH = 21
BOARD.setup()

reader = PackageReader()


class LoRaMaster(LoRa):
	def __init(self):
		super(LoRaRcvCont, self).__init__(verbose)
		self.set_mode(MODE.STDBY)
		#self.set_dio_mapping([0] * 6)
		self.db = AWS()

	def on_rx_done(self):
		BOARD.led_on()

		self.clear_irq_flags(RxDone=1)
		reader.read_package(self.read_payload(nocheck=True))

		self.set_mode(MODE.SLEEP)

		self.reset_ptr_rx()
		BOARD.led_off()
		self.set_mode(MODE.RXCONT)
		
		self.db.publish_sensor_data(reader.data_pack, True)


	def on_txdone(self):
		print("\nTxDone")
		print(self.get_irq_flags())

	def on_cad_done(self):
		print("\non_CadDone")
		print(self.get_irq_flags())

	def on_rx_timeout(self):
		print("\non_RxTimeout")
		print(self.get_irq_flags())
		time.sleep(.5)
		self.set_mode(MODE.SLEEP)
		self.reset_ptr_rx()
		self.set_mode(MODE.RXCONT)

	def on_valid_header(self):
		print("\non_ValidHeader")
		print(self.get_irq_flags())

	def on_payload_crc_error(self):
		print("\non_PayloadCrcError")
		print(self.get_irq_flags())

	def on_fhss_change_channel(self):
		print("\non_Fhss_changeChannel")
		print(self.get_irq_flags())

	def print_payload(self, payload):
		chex_sum = payload[0]
		cmd = payload[1]

		print("chex_sum: \t{}".format(chex_sum))
		print("payload len: \t{}".format(len(payload)))

		if (chex_sum == len(payload)):
			print("payload of correct length")
		else:
			print("payload of incorrect length")
		print("command: \t{}".format(cmd))


	def start(self):
		self.db = AWS()
		self.reset_ptr_rx()
		self.set_mode(MODE.RXCONT)
		self.db.connect()
		
		while True:
			time.sleep(.5)
			rssi_value = self.get_rssi_value()
			snr_value = self.get_pkt_snr_value()
			status = self.get_modem_status()
			sys.stdout.flush()
			sys.stdout.write("\r%d %d %d %d" % (rssi_value, snr_value, status['rx_ongoing'], status['modem_clear']))

lora = LoRaMaster()

try:
	#lora = LoRa(verbose=False, do_calibration=False)
	lora.set_mode(MODE.STDBY)

#	lora.set_freq(868.0)
	lora.set_freq(868.25)
	lora.set_coding_rate(CODING_RATE.CR4_5)
	lora.set_bw(BW.BW125)
	lora.set_spreading_factor(9)
	lora.set_pa_config(output_power=5)
	lora.set_preamble(12)
	lora.set_rx_crc(0)
	lora.set_implicit_header_mode(0)
	lora.set_max_payload_length(250)
	#lora.set_invert_iq(0)

	time.sleep(2)
except:
	print("Error in setup")
	print("Closing")
	BOARD.teardown()
	print("END")

#print("Version: \t{}".format(lora.get_version()))
#print("Frequency: \t{}MHz".format(lora.get_freq()))
#print("Modem Config 1: {}".format(lora.get_modem_config_1()))
#print("Modem Config 2: {}".format(lora.get_modem_config_2()))
#print("PA Config: \t{}".format(lora.get_pa_config()))

#lora.set_mode(MODE.RXSINGLE)

#print(lora)
#assert(lora.get_agc_auto_on() == 1)

# Start Listening

try:
	lora.start()
except KeyboardInterrupt:
	sys.stdout.flush()
	print("")
	sys.stderr.write("KeyboardInterrupt\n")
finally:
	sys.stdout.flush()
	print("")
	lora.set_mode(MODE.SLEEP)
	print(lora)
	BOARD.teardown()
	lora.db.disconnect()

#BOARD.teardown()
#print("END")
