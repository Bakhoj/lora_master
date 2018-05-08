import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from random import randint


#host = "/project/deviceSDK/public_key.pem.key"
#host = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz1P0zoL65wG9IF80+opBTNTXPQKN8fqFAyFeGiBA2oCzK+GYojr1lcjKYSV5GmcmCCV4bGi9R9SxzVHcxtse+1KEDL6zQzPg4YBNTUBBemq/XZy0MsB81UdmcoauQBSqSXXiYP67QNlYNeSrQtIOA31I67VP71/xyeDlBlVj3xOOagTVGk4oDAmfHF9n7u/DJZ0sLprgAj5u4pyL1E2w+UFnVOZy918h7InoRm9yqidllLfvzz5l+6KM5keBmmQxAerJwpxeF79xpGuiNJ/FIGv+asDO3NvbXb0XWpmYMy8fqsPRMLEYZcYw3ViNNrWB5H6NIGpaQWwbFx3P21G/cwIDAQAB"
host = "a3867rpfz9hgy1.iot.eu-central-1.amazonaws.com"
rootCAPath = "/project/deviceSDK/root_CA.pem"
privateKeyPath = "/project/deviceSDK/private_key.pem.key"
certificatePath = "/project/deviceSDK/certificate.pem.crt"


delay_s = 30
sensor_sn = '00000001'
topic = 'RaspPiTest_01/'+sensor_sn

loopCount = 1

myMQTTClient = None

try:

#	myMQTTClient = AWSIoTMQTTClient("RasPiTest_01", useWebsocket=True)
#	myMQTTClient.configureEndpoint(host, 443)
#	myMQTTClient.configureCredentials(rootCAPath)
	print("Creating Client")
	myMQTTClient = AWSIoTMQTTClient("RaspPiTest_01")
	myMQTTClient.configureEndpoint(host, 8883)
	myMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

#	myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
	myMQTTClient.configureOfflinePublishQueueing(-1)
	myMQTTClient.configureDrainingFrequency(2)
	myMQTTClient.configureConnectDisconnectTimeout(10)
	myMQTTClient.configureMQTTOperationTimeout(5)
	print("Connecting... ")
	myMQTTClient.connect()
	print("connected")
	time.sleep(2)




	#timestamp = datetime.datetime.now()
	#print(" Time: {} \n".format(timestamp))
	while True:
		temperature = randint(8, 32)
		timestamp = time.time()
#		dataID = "MS_" + timestamp + "_" + topic + "_something"
		dataID = "MS_{}_{}_something".format(timestamp, topic)

		msg = '"dataID": "{:s}", "device": "{:s}", "airTemperatur": "{}", "timestamp": "{}"'.format(dataID, sensor_sn, temperature, timestamp)
		msg = '{'+msg+'}'

		myMQTTClient.publish(topic, msg, 1)
		loopCount += 1
		print('Sleeping...')
		time.sleep(delay_s)
except KeyboardInterrupt:
	pass

print('Exiting the loop');
myMQTTClient.disconnect()
print('Disconnected from AWS')
