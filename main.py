import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

import threading
import json
import re

IPV4_PATTERN = "^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

number_of_repetations = 1
payload: dict
config: dict
client_list: list = []

def send_payload(client_list: list[mqtt.Client], dummys:int, delay: float, nore: int, payload):

    '''
        Handels the modification of the payload and starts the next timer for the next message

        Args:
            client (mqtt.Client): The mqtt connection
            dummys (int): Number of dummys for simulating devices
            delays (float): Seconds of wait time for the next message

        Returns:
            None
    '''

    payload = modify_timestamp(payload=payload, offset=config['offset'], nore=nore)

    # with open('topics.json', 'w', encoding='utf-8') as payload_file:
    #     json.dump(payload, payload_file, indent=4)

    for client in client_list:

        for device in range(1,dummys+1):

            # payload = modify_serial(payload=payload)

            for key, value in payload["Topics"].items():

                client.publish(key, json.dumps(value), qos=1)
                print(f'Message send to {client}')

    threading.Timer(delay, send_payload, args=(client_list, dummys, delay, number_of_repetations, payload)).start()

def modify_serial(payload: dict)->dict:

    '''
        Increments the serial_number (`sn`) by 1 for every entry in config.json parameter 'modules'.

        Args:
            payload (dict): The original payload dictionary

        Returns:
            dict: The modified payload with updated serial.
    '''

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

def modify_timestamp(payload:dict, offset:int, nore:int)->dict:

    '''
        Increments the timestamp (`ts`) by 1 for each topic in the payload.

        Args:
            payload (dict): The original payload dictionary

        Returns:
            dict: The modified payload with updated timestamps.
    '''


    for key, value in payload["Topics"].items():
        
        value['ts'] = value['ts'] + (offset * nore)

    return payload



if __name__ == "__main__":
    
    client = mqtt.Client(CallbackAPIVersion.VERSION2)

    with open('topics.json', encoding='utf-8') as payload_file:
        payload = json.load(payload_file)

    with open('config.json', encoding='utf-8') as config_file:
        config = json.load(config_file)

    # if config.get("username") and config.get("password"):
    #     client.username_pw_set(config["username"], config["password"])

    # if re.match(IPV4_PATTERN,config["IP"]):
    #     if config['Port'] in range(1, 65535):
    #         client.connect(config["IP"], config["Port"])
    #         print(f'Connected to Broker')
    #     else:
    #         print(f'Port in config.json not valid: {config["Port"]}')
    # else:
    #     print(f'IP in config.json not valid: {config["IP"]}')

    interval = config['interval']

    for ip in config["IP"]:
        if re.match(IPV4_PATTERN,ip):
            if config['Port'] in range(1, 65535):
                
                client = mqtt.Client(client_id=f"client_{ip}", callback_api_version=CallbackAPIVersion.VERSION2)
                if config.get("username") and config.get("password"):
                    client.username_pw_set(config["username"], config["password"])
                client.connect(ip, config["Port"])
                print(ip)
                client.loop_start()
                client_list.append(client)

                print(f'Connected to Broker')
            else:
                print(f'Port in config.json not valid: {config["Port"]}')
        else:
            print(f'IP in config.json not valid: {ip}')        

    

    threading.Timer(interval, send_payload, args=(client_list,config['modules'], interval, number_of_repetations, payload)).start()

    client.loop_start()