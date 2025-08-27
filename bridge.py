import asyncio
import websockets
import paho.mqtt.client as mqtt

MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "factory/machine1/status"
WS_PORT = 8765

latest_message = "System Starting..."

# MQTT callbacks
def on_message(client, userdata, msg):
    global latest_message
    latest_message = msg.payload.decode()

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

# WebSocket server
async def ws_handler(websocket):
    global latest_message
    while True:
        await websocket.send(latest_message)
        await asyncio.sleep(1)

# start_server = websockets.serve(ws_handler, "localhost", WS_PORT)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

async def main():
    # Create server with correct signature
    async with websockets.serve(ws_handler, "localhost", 8765):
        print("✅ WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())