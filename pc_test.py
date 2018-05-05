from weather_master import PackageReader

print("Start Master Module Simulator")

reader = PackageReader()

print("\nRxDone")

payload = [0x09, 0x05, 0x2E, 0x95, 0xF3, 0x71, 0x80, 0x00, 0x62]


print(bytes(payload).hex())

reader.read_package(payload, True)
print("Accepted payload: ", reader.is_accepted())