import network
import time
import socket
from machine import ADC, Pin
from time import sleep

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            time.sleep(1)

    print('Connected to WiFi')
    print('Network config:', wlan.ifconfig())

def send_adc_data(host, port, sample_rate):
    adc_pin = ADC(Pin(26))

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
                
                # Assuming your MAX4466 output is within the 0-3.3V range
                # Map the ADC value to a voltage between 0 and 3.3V
                voltage = (audio_value / 4095) * 3.3
                voltage_int = int(voltage * 1000) 
                # Now send the voltage value to the client
                client_socket.send(voltage_int.to_bytes(2, "little"))

        except OSError as e:
            if e.errno == 98:  # EADDRINUSE
                print(f"Port {port} is in use. Retrying in 5 seconds...")
                sleep(5)
            else:
                raise

if __name__ == "__main__":
    wifi_ssid = 'Max44663'
    wifi_password = 'RaspberryPi9911@'
    connect_to_wifi(wifi_ssid, wifi_password)

    HOST = "0.0.0.0"  # Listen on all available interfaces
    PORT = 80

    SAMPLE_RATE = 44100  
    send_adc_data(HOST, PORT, SAMPLE_RATE)

