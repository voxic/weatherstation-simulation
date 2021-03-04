# Simulation of weather data

This simple application simulates

- Temperature
- Wind
- Rain

To run, you will need Python version 3.5 or above
Python library Paho-mqtt https://pypi.org/project/paho-mqtt/

Run:
```bash

python main.py

```

Configuration:  
Change variables in the beginning of the file

```python

# Set this to the IP of your service domain
service_domain_ip = "10.0.0.18" <---

# Set device name
device_name = "dev002" <---

# Set MQTT topic, this need to be the same that Data sources is pointing to.
topic = "weather/data" <---

# Download certificates from your service domain. This is done under Data sources and IoT Sensors at https://karbon.nutanix.com
# Place the certificates in the same folder as the script
ca = "ca.crt" # Root CA file <---
cert = "cert.crt" # Certificate <---
private = "key.key" # Private key <---

```

This simulation publishes the following packet structure to the configured MQTT topic:

```json

{
    "device":"dev001",
    "measurement":"temperature",
    "value":"0.3",
    "ts":1614801607246
}

```

Written by Emil Nilsson @ 2020