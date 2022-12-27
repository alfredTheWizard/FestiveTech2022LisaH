# Install the following dependencies on your PI to get started
# sudo apt-get install python-dev
# sudo apt update
# sudo apt install git
# sudo apt-get install build-essential python-dev
# sudo apt-get install python3-setuptools
# sudo apt install python3-pip

# Adafruit_DHT specific dependencies 
# git clone https://github.com/adafruit/Adafruit_Python_DHT.git
# cd Adafruit_DHT/
# sudo python3 setup.py install
# sudo pip3 install Adafruit-DHT

#Twilio specific dependency
# How to buy a Twilio Phonenumber https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account#:~:text=Get%20your%20first%20Twilio%20phone%20number,-You%20will%20need&text=After%20signing%20up%20for%20your,%2C%20MMS%2C%20and%20Fax).
# pip3 install twilio

# Azure IoT Hub specific dependency 
# pip3 install azure-iot-device

# Example code to read from Adafruit Sensor
import Adafruit_DHT

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 17) #17 refers to the number of the data pin used! 
humidity = round(humidity, 2)
temperature = round(temperature, 2)

# Example code to make a call using Twilio
# How to buy a Twilio Phonenumber https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account#:~:text=Get%20your%20first%20Twilio%20phone%20number,-You%20will%20need&text=After%20signing%20up%20for%20your,%2C%20MMS%2C%20and%20Fax).
from twilio.rest import Client
account_sid = '<account_sid>'
auth_token = '<auth_token>'
phonenumber_to = '<phonenumber_to_including_country_code>'
phonenumber_from = '<phonenumber_from_including_country_code>'

twillio_client = Client(account_sid, auth_token)

humidity = 60
temperature = 36

twillio_client.calls.create(twiml='<Response><Say>Hi Lisa, There is something wrong with the terrarium. The humidity is ' + str(humidity) + 
								  ' and the ambient temperature is ' + str(temperature) + '. Please act now </Say></Response>',
							to=phonenumber_to,
							from_=phonenumber_from
							)

# Example code to send data to IoT Hubs
from azure.iot.device import IoTHubDeviceClient, Message
connection_string = '<connection_string>'

iothub_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

msg_txt_formatted = "{'temperature': 36, 'humidity': 65}"
message = Message(msg_txt_formatted)

message.content_encoding = "utf-8"
message.content_type = "application/json"

iothub_client.send_message(message)


