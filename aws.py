import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


#host = "/project/deviceSDK/public_key.pem.key"
host = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz1P0zoL65wG9IF80+opBTNTXPQKN8fqFAyFeGiBA2oCzK+GYojr1lcjKYSV5GmcmCCV4bGi9R9SxzVHcxtse+1KEDL6zQzPg4YBNTUBBemq/XZy0MsB81UdmcoauQBSqSXXiYP67QNlYNeSrQtIOA31I67VP71/xyeDlBlVj3xOOagTVGk4oDAmfHF9n7u/DJZ0sLprgAj5u4pyL1E2w+UFnVOZy918h7InoRm9yqidllLfvzz5l+6KM5keBmmQxAerJwpxeF79xpGuiNJ/FIGv+asDO3NvbXb0XWpmYMy8fqsPRMLEYZcYw3ViNNrWB5H6NIGpaQWwbFx3P21G/cwIDAQAB"
rootCAPath = "/project/deviceSDK/root_CA.pem"
privateKeyPath = "/project/deviceSDK/certificate.pem.crt"
certificatePath = "/project/deviceSDK/private_key.pem.key"


delay_s = 60
sensor_sn = '00000001'
topic = 'myrpi/'+sensor_sn

temperature = 56
loopCount = 2

try:

#	myMQTTClient = AWSIoTMQTTClient("RasPiTest_01", useWebsocket=True)
#	myMQTTClient.configureEndpoint(host, 443)
#	myMQTTClient.configureCredentials(rootCAPath)

	myMQTTClient = AWSIoTMQTTClient("RaspTiTest_01")
	myMQTTClient.configureEndpoint(host, 8883)
	myMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

#	myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
	myMQTTClient.configureOfflinePublishQueueing(-1)
	myMQTTClient.configureDrainingFrequency(2)
	myMQTTClient.configureConnectDisconnectTimeout(10)
	myMQTTClient.configureMQTTOperationTimeout(5)

	myMQTTClient.connect()

	time.sleep(2)




	timestamp = datetime.datetime.now()
	print(" Time: {} \n".format(timestamp))

	msg = '"Device": "{:s}", "Temperature": "{}", "Loop": "{}"'.format(sensor_sn, temperature, loopCount)
	msg = '{'+msg+'}'

	myAWSIotMQTTClient.publish(topic, msg, 1)

	print('Sleeping...')
	time.sleep(delay_s)
except KeyboardInterrupt:
	pass

print('Exiting the loop');
myAWSIoTMQTTClient.disconnect()
print('Disconnected from AWS')
