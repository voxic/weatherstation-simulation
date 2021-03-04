#
# * Project: Weatherstation-simulation
# * File: main.py
# * Author: Emil Nilsson
# * Contact: emil.nilsson@nutanix.com
#

## Imports
import sys
import ssl
import time
import datetime
import logging, traceback
import paho.mqtt.client as mqtt
import random
import json
import math


# Set this to the IP of your service domain
service_domain_ip = "10.0.0.18"

# Set device name
device_name = "dev002"

# Set MQTT topic, this need to be the same that Data sources is pointing to.
topic = "weather/data"

# Download certificates from your service domain. This is done under Data sources and IoT Sensors at https://karbon.nutanix.com
# Place the certificates in the same folder as the script
ca = "ca.crt" # Root CA file
cert = "cert.crt" # Certificate
private = "key.key" # Private key

# Setup logger
logger = logging.getLogger() 
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

# Set base values
last_temp = 20.0
last_wind = 0.10
last_rain = 0.00

# Create ssl_context
def ssl_alpn():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.verify_mode = ssl.CERT_OPTIONAL 
        ssl_context.check_hostname = False        # hostname checking needs to be disabled, as the certificate is signed by the service domain (127.0.0.1)
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private, )

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

if __name__ == '__main__':

    # Connect to Service domain MQTT
    try:
        mqttc = mqtt.Client()
        ssl_context= ssl_alpn()
        mqttc.tls_set_context(context=ssl_context)
        logger.info("start connect")
        mqttc.connect(service_domain_ip, port=1883)
        logger.info("connect success")
        mqttc.loop_start()

        # Main Loop
        while True:
            ts = round(time.time()*1000)
            # Generate Temperature values
            new_temp = last_temp + (random.randint(-20, 20) / 100)
            new_temp = round(new_temp, 1)
            newPayload = {"device" : device_name, "ts" : ts, "measurement" : "temperature","value" : str(new_temp)}
            mqttc.publish(topic, json.dumps(newPayload)) # Publish to broker
            logger.info("try to publish:{}".format(newPayload))

            # Generate Wind values
            new_wind = last_wind + (random.randint(-20, 20) / 100)
            new_wind = round(new_wind, 2)
            if(new_wind < 0):
                new_wind = 0.00
            newPayload = {"device" : device_name, "ts" : ts, "measurement" : "wind","value" : str(new_wind)}
            mqttc.publish(topic, json.dumps(newPayload)) # Publish to broker
            logger.info("try to publish:{}".format(newPayload))

            # Generate Rain values, rain is only sent if it is over 1 mm
            new_rain = last_rain + (random.randint(-50, 50) / 100)
            new_rain = round(new_rain, 1)
            if(new_rain < 0):
                new_rain = 0.00
            if(new_rain > 1.0):
                newPayload = {"device" : device_name, "ts" : ts, "measurement" : "rain","value" : str(new_rain)}
                mqttc.publish(topic, json.dumps(newPayload))
                logger.info("try to publish:{}".format(newPayload))            

            # Set new base value for next round
            last_temp = new_temp
            last_wind = new_wind
            last_rain = new_rain

            # Set time between data points
            time.sleep(1)

    except Exception as e:
        logger.error("exception main()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)