import network
from machine import Pin
import time

# Wi-Fi configuration
ssid = "abc"
password = "xyz"

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep_ms(500)
            print("Connecting to WiFi...")
    print("Connected to Wi-Fi")

try:
    connect_to_wifi()
except KeyboardInterrupt:
    print("Program terminated")

