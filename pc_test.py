from weather_master import PackageReader
from aws import AWS

print("Start Master Module Simulator")

reader = PackageReader()

print("\nRxDone")

payload = [0x0A, 0x05, 0x2E, 0x95, 0xF3, 0x71, 0x84, 0x00, 0x62, 0x11]


print(bytes(payload).hex())

reader.read_package(payload, True)

db = AWS()

db.connect()
db.publish_sensor_data(reader.data_pack, True)
db.disconnect()