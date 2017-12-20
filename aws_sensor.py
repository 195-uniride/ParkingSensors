import json
import logging

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

logging.basicConfig()

def broadcast(state):
	myMQTTClient = AWSIoTMQTTClient("Linux-laptop")

	myMQTTClient.configureEndpoint("avvvr84optu81.iot.us-west-2.amazonaws.com", 8883)

	root_ca_path = "/home/akshat/.local/aws_device_cert/root-CA.crt"
	private_key_path = "/home/akshat/.local/aws_device_cert/Linux-laptop.private.key"
	certificate_path = "/home/akshat/.local/aws_device_cert/Linux-laptop.cert.pem"
	myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

	myMQTTClient.configureOfflinePublishQueueing(-1)
	myMQTTClient.configureDrainingFrequency(2) 
	myMQTTClient.configureConnectDisconnectTimeout(10) 
	myMQTTClient.configureMQTTOperationTimeout(5)

	def customCallback(client, userdata, message):
	    print("Received a new message: ")
	    print(message.payload)
	    print("from topic: ")
	    print(message.topic)
	    print("--------------\n\n")

	myMQTTClient.connect()
	myMQTTClient.subscribe("spot/state", 1, customCallback)
	if(state==0):
		data = {
			    "state": {
			        "reported": {
			            "spot": "constant"
			        }
			    }
			}
	elif(state==1):
		data = {
			    "state": {
			        "reported": {
			            "spot": "entering"
			        }
			    }
			}
	elif(state==2):
		data = {
			    "state": {
			        "reported": {
			            "spot": "leaving"
			        }
			    }
			}
	myMQTTClient.publish("spot/state", json.dumps(data), 0)
	myMQTTClient.unsubscribe("ubuntu/clicker")
	myMQTTClient.disconnect()

if __name__=="__main__":
	broadcast(0)

 # python basicPubSub.py -e avvvr84optu81.iot.us-west-2.amazonaws.com 
 # -r /home/akshat/.local/aws_device_cert/root-CA.crt -c /home/akshat/.local/aws_device_cert/Linux-laptop.cert.pem 
 # -k /home/akshat/.local/aws_device_cert/Linux-laptop.private.key -id Linux-laptop
