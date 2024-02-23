import network
from machine import Pin
import time
from umqtt.simple import MQTTClient

# Wi-Fi configuration
ssid = "abc"
password = "xyz"

# MQTT configuration (use the public Mosquitto test broker)
mqtt_broker = "broker.emqx.io" #"mqtt://test.mosquitto.org"
mqtt_port = 1883
mqtt_topic = b"smart/mqtt"

# MQTT client configuration
client_id = f'raspberry-pub-{time.time_ns()}'
mqtt_client = MQTTClient(client_id, mqtt_broker, mqtt_port, "nawaraj", "password")

# PIR motion sensor configuration
pir = Pin(16, Pin.IN)
led = Pin("LED", Pin.OUT)
isMotionDetected = False
index = 0

def detect_motion(pir):
    global isMotionDetected
    isMotionDetected = True

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep_ms(500)
            print("Connecting to WiFi...")
    print("Connected to Wi-Fi")

def connect_to_mqtt():
    try:
        mqtt_client.connect()
        print("Connected to MQTT broker")
    except Exception as e:
        print("Error connecting to MQTT broker:", e)

def send_mqtt_message(topic, message):
    try:
        mqtt_client.publish(topic, message)
        print("Message published to MQTT topic:", topic)
    except Exception as e:
        print("Error publishing message to MQTT:", e)

pir.irq(trigger=Pin.IRQ_RISING, handler=detect_motion)

try:
    connect_to_wifi()
    connect_to_mqtt()

    while True:
        if isMotionDetected:
            print("Motion detected!")

            # Send MQTT message
            send_mqtt_message(mqtt_topic, b"Motion detected!")

            # Additional logic from the PIR motion sensor code
            isMotionDetected = False
            index += 1
            send_mqtt_message(mqtt_topic, b"Hey you have got a new mail".format(index))
            print("{} Hey you have got a new mail".format(index))
            led.toggle()

            # Add a delay to avoid multiple triggers in quick succession
            time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated")

