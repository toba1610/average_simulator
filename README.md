# Average Simulator 

A basic script to generate data points per mqtt for testing data handling on other devices.

To run the script to JSON are needed:
* config.json
* topic.json

## configs.json

* IP: STRING = The IP-Adress of the used broker. Be causios there is no input validation
* Port: STRING = The Port used by the mqtt broker
* username: STRING = If an autantification is used
* password: STRING = If an autantification is used
* interval: FLOAT = The interval in which the dummy message should be send
* modules: INTEGER = Defines how often a the messages should be send with differents serial each interval

### Example

```yaml
    {
        "IP": "192.168.178.42",
        "Port": 8080,
        "username": "",
        "password": "",
        "interval": 1,
        "modules": 1
    }
```
## topics.json

This json contains all the topic whichshould be send each interval.
The json is structured as an array of objects. The objects contains the topic path as key and the payload as value.

### Example:

```yaml
"Topics": {
        "EM3X/100009/EMAVG": {
            "avi": [
                32.367,
                24.948,
                36.824,
                31.722
            ],
            "avv": [
                -38.206,
                -20.997,
                72.404
            ]
        }
    }
```