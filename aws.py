import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from random import randint
from data_pack import DataPack
#from simple_time import SimpleTime



class AWS():
	__host = "a3867rpfz9hgy1.iot.eu-central-1.amazonaws.com"
	__rootCAPath = "deviceSDK/root_CA.pem"
	__privateKeyPath = "deviceSDK/private_key.pem.key"
	__certificatePath = "deviceSDK/certificate.pem.crt"

	def __init__(self):
		self.client = None
		self.master_id = '123456783245'

	def connect(self, verbose = False):
		if verbose:
			print("Connecting...")
		try:
			self.client = AWSIoTMQTTClient("RaspPiTest_01")
			self.client.configureEndpoint(AWS.__host, 8883)
			self.client.configureCredentials(AWS.__rootCAPath, AWS.__privateKeyPath, AWS.__certificatePath)
			#self.client.configureAutoReconnectBackoffTime(1, 32, 20)
			self.client.configureOfflinePublishQueueing(-1)
			self.client.configureDrainingFrequency(2)
			self.client.configureConnectDisconnectTimeout(10)
			self.client.configureMQTTOperationTimeout(5)
			self.client.connect()
			time.sleep(2)
		except Exception:
			if verbose:
				print("Connection failed")

	def publish_sensor_data(self, data_pack: DataPack, verbose = False):
		#timestamp = time.time()

		topic = 'RaspPiTest_01/sensor_data'
		dataID = "SD_{}_{}_{}".format(data_pack.time.to_float_time(), self.master_id, data_pack.station_id)

		msg = '"dataID": "{:s}", "timestamp": "{}", "stationID": "{}", "masterID": "{}"'.format(dataID, data_pack.time.to_float_time(), data_pack.station_id, self.master_id)

		data_pack.buildDict()
		for key, value in data_pack.dict.items():
			msg += ', "{:s}": "{}"'.format(key, value)
		msg = '{'+msg+'}'

		if verbose: print("Sending Data...")

		self.client.publish(topic, msg, 1)

		if verbose: print("Data send")

	def disconnect(self, verbose = False):
		self.client.disconnect()
