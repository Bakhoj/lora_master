from simple_time import SimpleTime
from data_pack import DataPack

"""
Time to connect the Module to the DB http://www.fhilitski.com/2016/11/temperature-sensor-with-raspberry-pi-3-and-aws/ 
"""


class PackageReader():
	def __init__(self):
		pass

	def read_package(self, payload, verbose = False):
		if(type(payload) is not list):
			print("Wrong payload type")
			return
		self.data_pack = DataPack()
		self.verbose = verbose
		self.index = 0
		self.payload = payload
		self.chex_sum = self.payload[self.inc()]
		self.cmd = self.payload[self.inc()]
		self.accepted_package = self.chex_sum == len(payload)

		if(self.verbose):
			print("\n==================================")
			print("chex_sum: \t", self.chex_sum)
			print("command: \t", self.cmd)

		if(self.accepted_package == False):
			if(self.verbose):
				print("Package not accepted")
				print("==================================\n")
			return
		
		self.__cmd_lookup(self.cmd)

	def read_package_async(self, payload):
		self.read_package(payload, verbose=False)

	def is_accepted(self):
		return self.accepted_package

	
	def __cmd_lookup(self, x):
		if x == 0x01:
			#Local Station ID Request S -> M
			pass
		elif x == 0x02:
			#Local Station ID Response M -> S
			pass
		elif x == 0x03:
			#Local Time ID Request S -> M
			pass
		elif x == 0x04:
			#Local Time ID Respons M -> S
			pass
		elif x == 0x05:
			#Send measured station data
			self.__cmd_sensor_data()
		elif x == 0x06:
			#Received measured station data
			pass
		elif x == 0x07:
			#Send Undifined data?
			pass
		elif x == 0x08:
			#Send Station Status
			pass
		elif x == 0x09:
			#Received Station Status
			pass
		else:
			self.__invalid_command()

	def __cmd_sensor_data(self):
		if(self.verbose):
			print("\n==================================")
			print("\tSensor Data command")
		self.__record_station_id()
		self.__record_time_id()
		self.__check_available_sensors()
		self.__record_sensor_data()

		if(self.verbose):
			print("==================================\n")

	def __record_station_id(self):
		self.data_pack.station_id = (self.payload[2] << 8)+ self.payload[3]
		if(self.verbose):
			print("Local Station Identification: \t", self.data_pack.station_id)

	def __record_time_id(self):
		self.data_pack.time.byte_to_time(self.payload[4], self.payload[5])
		if(self.verbose):
			print("Local Times Identification: \t{}:{}:{}".format(self.data_pack.time.day, self.data_pack.time.hour, self.data_pack.time.minute))

	def __check_available_sensors(self):
		"""
		will set the booleans for sensor data, 
		and set the self.index to 8 and makes it ready for __record_sensor_data.
		self.verbose will print sensors availability.
		"""
		sensor_byte_one = self.payload[6]
		sensor_byte_two = self.payload[7]
		self.index = 8

		self.data_pack.has_bat_lvl = self.__bit_check(sensor_byte_one)(8)

		self.data_pack.has_air_temp = self.__bit_check(sensor_byte_one)(4)
		self.data_pack.has_air_hum = self.__bit_check(sensor_byte_one)(3)
		
		if(self.verbose):
			print("Has battery level: \t", self.data_pack.has_bat_lvl)
			print("Has air temperature: \t", self.data_pack.has_air_temp)
			print("Has air humidity: \t", self.data_pack.has_air_hum)

	def __record_sensor_data(self):
		verbose = self.verbose
		# 1. Battery level
		if self.data_pack.has_bat_lvl: 
			self.data_pack.bat_lvl = self.payload[self.inc()]
			if verbose:
				print("Battery level: \t\t", self.data_pack.bat_lvl)

		# 5. Air Temperature
		if self.data_pack.has_air_temp: 
			self.data_pack.air_temp = self.payload[self.inc()]
			if verbose:
				print("Air temperature: \t", self.data_pack.air_temp)

		# 6. Air Humidity
		if self.data_pack.has_air_hum: 
			self.data_pack.air_hum = self.payload[self.inc()]
			if verbose:
				print("Air humidity: \t\t", self.data_pack.air_hum)


	def __invalid_command(self):
		if(self.verbose):
			print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			print("\tInvalid command")
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")

	def __bit_check(self, x): 
		""" 
		x: Number to chekc
		n: bit to check from right most bit to left (1-8)
		"""		
		return lambda n: 0 < (x & (1 << (n - 1)))
	
	def inc(self):
		self.index += 1
		return self.index - 1