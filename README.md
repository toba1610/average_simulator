# Average Simulator 

A basic script to generate data points per mqtt for testing data handling on other devices.

To run the script to JSON are needed:
* config.json
* topic.json

## configs.json

Be causios there is no input validation for any Parameter.

| Parameter        | Type       | Explanation  |
| ------------- |:-------------:| :-----|
| IP      | STRING | The IP-Adress of the used broker |
| Port      | INTEGER      |   The Port used by the mqtt broker |
| username | STRING      |    If an autantification is used, else "" |
| password | STRING      |    If an autantification is used, else "" |
| interval | FLOAT      |    The interval in which the dummy message should be send |
| modules | INTEGER      |    Defines how often the messages should be send with differents serial each interval |

### Example

```json
    {
        "IP": "192.168.178.42",
        "Port": 1883,
        "username": "",
        "password": "",
        "interval": 1,
        "modules": 1
    }
```
## topics.json

This json contains all the topics which should be sent each interval.
The json is structured as an array of objects. The objects contain the topic path as key and the payload as value.

### Example:

```json
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