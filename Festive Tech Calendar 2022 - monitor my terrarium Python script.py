# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import Adafruit_DHT
from azure.iot.device import IoTHubDeviceClient, Message
from twilio.rest import Client
import argparse

def read_adafruit_sensor():
    # This function reads temperature/humidity data from the humidity sensor
    try:
        # GPIO17
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 17)
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print(f"the temperature = {str(temperature)} and the humidity = {str(humidity)}" )

        return round(temperature, 2), round(humidity, 2)
    except Exception as e:
        body_text = "The adafruit sensor cannot be read, returning a tuple containing 0's with errorcode " + str(e)
        print(body_text)
        return 0, 0

def check_sensor_and_alert(ambient_temp, humidity):
    try:
        # check ambienttemp
        if ambient_temp > 40:
            print(f'ambient temperature is too high: {ambient_temp}')
            call_lisa_using_alert(ambient_temp, humidity, phonenumber_to, phonenumber_from)
        elif ambient_temp < 20:
            print(f'ambient temperature is too low: {ambient_temp}')
            call_lisa_using_alert(ambient_temp, humidity, phonenumber_to, phonenumber_from)
        else:
            print(f'ambient temperature is sufficient: {str(ambient_temp)}')

        if humidity > 80:
            print(f'humidity is too high: {str(humidity)}')
            call_lisa_using_alert(ambient_temp, humidity, phonenumber_to, phonenumber_from)
        elif ambient_temp < 55:
            print(f'humidity is too low: {str(humidity)}')
            call_lisa_using_alert(ambient_temp, humidity, phonenumber_to, phonenumber_from)
        else:
            print(f'ambient temperature is sufficient: {str(humidity)}')       

    except Exception as e:
        body_text = "raspberry pi was unable to do one of the checks with errorcode " + e
        print(body_text)

def call_lisa_using_alert(temperature, humidity, phonenumber_to, phonenumber_from):
    # This functions calls Lisa usihng a Twillio phone number
    twillio_client = Client(account_sid, auth_token)
    temperature = str(temperature)
    humidity = str(humidity)

    twillio_client.calls.create(twiml='<Response><Say>Hi Lisa, There is something wrong with the terrarium. The humidity is ' + str(humidity) + 
								  ' and the ambient temperature is ' + str(temperature) + '. Please act now </Say></Response>',
							to=phonenumber_to,
							from_=phonenumber_from
							)
    print("called Lisa")


# AZURE IOT HUB FUNCTIONS #
def iothub_client_init():
    # Create an IoT Hub client, used for sending telemetry data
    iothub_client = IoTHubDeviceClient.create_from_connection_string(
        connection_string)

    return iothub_client


def iothub_client_send_telemetry(ambienttemp, humidity):
    # This function creates a json message from the collected telemetry data
    # and sends it to the Azure IOT hub
    try:
        msg_txt_formatted = "{'temperature': {ambienttemp}, 'humidity': {humidity}}"
        message = Message(msg_txt_formatted)

        message.content_encoding = "utf-8"
        message.content_type = "application/json"

        iothub_client.send_message(message)
    except Exception as e:
        body_text = "raspberry pi was unable to send telemetry with errorcode " + str(e)
        print(body_text)


def loop():
    try:
        print("reading sensor")
        ambient_temp_humidity = read_adafruit_sensor()
        print("checking sensors")
        check_sensor_and_alert(ambient_temp_humidity[0], ambient_temp_humidity[1])
        print("sending output to IoT Hub")
        iothub_client_send_telemetry(ambient_temp_humidity[0], ambient_temp_humidity[1])
        print("ready for the next loop")

        # sleep 15 mins
        time.sleep(900)

    except Exception as e:
        body_text = "something is wrong with the pi, and other functions did not catch the error, with errorcode " + str(e)
        print(body_text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--account_sid", type=str, help='help')
    parser.add_argument("--auth_token", type=str, help='help')
    parser.add_argument("--connection_string", type=str, help='help')
    parser.add_argument("--phonenumber_from", type=str, help='help')
    parser.add_argument("--phonenumber_to", type=str, help='help')
    namespace = parser.parse_args()

    account_sid = namespace.account_sid
    auth_token = namespace.auth_token
    connection_string = namespace.connection_string
    phonenumber_from = namespace.phonenumber_from
    phonenumber_to = namespace.phonenumber_to

    try:
        iothub_client = iothub_client_init()
        true = True
        while true:
            loop()
    except Exception as f:
        true = True
        while true:
            body1 = "something is wrong with the pi, and other functions did not catch the error"
            print(body1)
            time.sleep(900)

    except KeyboardInterrupt:
        quit()
