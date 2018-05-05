class PackageReader():
	def __init__(self):
		self.chex_sum = 0
		pass

	def read_package(self, payload, verbose = False):
		if(type(payload) is not list):
			print("Wrong payload type")
			return
		self.chex_sum = payload[0]
		self.cmd = payload[1]
		self.accepted_package = self.chex_sum == len(payload)

		if(verbose):
			print("chex_sum: \t", self.chex_sum)
			print("command: \t", self.cmd)

	def read_package_async(self, payload):
		self.read_package(payload, verbose=False)
		pass

	def is_accepted(self):
		return self.accepted_package




