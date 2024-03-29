import datetime
import requests

ORION_URL = "http://localhost:1026/v2/entities"

def process_message(message):
    time = datetime.datetime.fromtimestamp(message["time"]/1000).isoformat()
    print("Received message:", str(message["temp"]) + "°C", time)

    ngsi_entity = {
        "id": "urn:ngsi-v2:Sensor:1",
        "type": "SensorReading",
        "temperature": {
            "type": "Number",
            "value": message["temp"],
        },
        "timestamp": {
            "type": "DateTime",
            "value": time,
        }
    }
    return ngsi_entity

def post_or_update_entity(entity):
    headers = {
        "Content-Type": "application/json",
    }

    # Check if the entity exists
    response = requests.get(ORION_URL + "/" + entity["id"])  # Removed headers=headers
    if response.status_code == 200:
        print("EXITS")
        # If it exists, update the entity
        # Create a new dictionary excluding the 'id' and 'type' fields
        entity_for_update = {key: entity[key] for key in entity if key not in ['id', 'type']}
        response = requests.patch(ORION_URL + "/" + entity["id"] + "/attrs", headers=headers, json=entity_for_update)
        if response.status_code == 204:
            print("Entity updated successfully.")
        else:
            print("Failed to update entity:", response.status_code, response.text)
    elif response.status_code == 404:
        # If it doesn't exist, create the entity
        print("DOES NOT EXIST")
        response = requests.post(ORION_URL, headers=headers, json=entity)
        if response.status_code == 201:
            print("Entity created successfully.")
        else:
            print("Failed to create entity:", response.status_code, response.text)
    else:
        print("Failed to get entity:", response.status_code, response.text)


def create_subscription():
    headers = {
        "Content-Type": "application/json",
    }
    subscription = {
        "description": "Notify QuantumLeap",
        "subject": {
            "entities": [
                {
                    "id": "urn:ngsi-v2:Sensor:1",
                    "type": "SensorReading"
                }
            ],
            "condition": {
                "attrs": ["temperature"],
                "expression": {
                    "q": "temperature>20"
                }
            }
        },
        "notification": {
            "http": {
                "url": "http://quantumleap:8668/v2/notify"
            },
            "attrs": ["temperature", "timestamp"],
            "metadata": ["dateCreated", "dateModified"]
        },
        "throttling": 5
    }

    response = requests.post("http://localhost:1026/v2/subscriptions", headers=headers, json=subscription)
    if response.status_code == 201:
        print("Subscription created successfully.")
    else:
        print("Failed to create subscription:", response.status_code, response.text)


def get_historical_data(entity_id):
    #get the historical data from quantumleap
    print("Getting historical data...")
    response = requests.get("http://localhost:8668/v2/entities/" + entity_id)
    if response.status_code == 200:
        print("Historical data:", response.json())
    else:
        print("Failed to get historical data:", response.status_code, response.text)
