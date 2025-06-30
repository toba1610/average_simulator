import paho.mqtt.client as mqtt
import threading
import json


def send_payload(client: mqtt.Client):

    with open('payload.json', 'r') as payload_file:
        payload = json.load(payload_file)

    for key, value in payload["Topics"].items():

        client.publish(key, value, qos=1)

    threading.Timer(1.0, send_payload, args=(client,)).start()




if __name__ == "__main__":
    
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    client = mqtt.Client()

    if config.get("username") and config.get("password"):
        client.username_pw_set(config["username"], config["password"])

    client.connect(config["IP"], config["Port"])

    interval = config['interval']

    threading.Timer(interval, send_payload, args=(client,config['modules'])).start()

    client.loop_start()