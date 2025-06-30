import paho.mqtt.client as mqtt
import threading
import json


def send_payload(client: mqtt.Client, dummys:int):

    with open('topics.json', 'r') as payload_file:
        payload = json.load(payload_file)

    payload = modify_timestamp(payload=payload)

    for device in range(1,dummys+1):

        payload = modify_serial(payload=payload)

        for key, value in payload["Topics"].items():

            client.publish(key, json.dumps(value), qos=1)

    threading.Timer(1.0, send_payload, args=(client, dummys,)).start()
def modify_serial(payload: dict)->dict:

    key:str
    new_topics = {}
    for key, value in payload["Topics"].items():
        key_seperated = key.split('/')
        new_key = str(int(key_seperated[1]) + 1)
        new_key = f'{key_seperated[0]}/{new_key}/{key_seperated[2]}'
        value['sn'] = new_key
        new_topics[new_key] = value
    payload["Topics"] = new_topics
    return payload

def modify_timestamp(payload:dict)->dict:

    for key, value in payload["Topics"].items():
        
        value['ts'] = value['ts'] + 1

    return payload

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