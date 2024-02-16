import machine
import utime
import network
import time
import socket
from machine import ADC, Pin

sensor_temp = machine.ADC(27)

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            time.sleep(1)

    print("Connected to WiFi")
    print("Network config:", wlan.ifconfig())

def send_adc_data(host, port):
    adc_pin = ADC(Pin(27))

    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen()

            print(f"Listening on {host}:{port}")

            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            while True:
                audio_value = adc_pin.read_u16()
                client_socket.send(audio_value.to_bytes(2, "little"))

            """except OSError as e:
            if e.errno == 98:  # EADDRINUSE
                print(f"Port {port} is in use. Retrying in 5 seconds...")
                sleep(5)
            else:
                raise"""
        except:
            print("Retrying...")
if __name__ == "__main__":
    wifi_ssid = "DESKTOP"
    wifi_password = "00000000"
    connect_to_wifi(wifi_ssid, wifi_password)

    HOST = "0.0.0.0"  # Listen on all available interfaces
    PORT = 87

    send_adc_data(HOST, PORT)

