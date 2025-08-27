import random
import time

import joblib

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("test.mosquitto.org", 1883)

def broadcast_status(temp, action):
    message = f"{temp},{action}"
    client.publish("factory/machine1/status", message)
    print(f"[Comm] Broadcast: {message}")

model = joblib.load("cooling_model.pkl")

def should_cool(temp):
    # Model expects input as [[value]]
    decision = model.predict([[temp]])[0]
    return decision

def read_temperature():
    # Simulated sensor reading
    return 25 + random.uniform(-2, 8)  # fluctuates between 23-33 °C

while True:
    try:
        temp = read_temperature()
        print(f"[Sensor] Current Temperature: {temp:.2f} °C")
        action = should_cool(temp)
        if action == 1:
            print("[Action] Cooling system ACTIVATED")
            # GPIO or relay code here
        else:
            print("[Action] System running NORMAL")
        broadcast_status(temp, action)
        time.sleep(5)
    except KeyboardInterrupt:
        print("safe exit")
        break