import network , socket
import _thread
import machine
import time


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


audio_value = 0

def read_ADC():
    adc_pin = machine.ADC(27)
    machine.ADC.atten(ADC.ATTN_0DB)
    """
    ADC.init(sample_ns=40, atten="0db")
    ADC.ATTN_0DB: No attenuation (1V).
    ADC.ATTN_2_5DB: 2.5 dB attenuation (1.34V).
    ADC.ATTN_6DB: 6 dB attenuation (2V).
    ADC.ATTN_11DB: 11 dB attenuation (3.6V).
    ADC.width(ADC.WIDTH_12BIT)
    from machine import Pin, ADC
    from time import sleep

    pot = ADC(Pin(34))
    pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v
    """
    global audio_value
    while True:
        audio_value = adc_pin.read_u16()
    
def send_adc_data(host, port):
    
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen()

            print(f"Listening on {host}:{port}")

            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            global audio_value
            while True:
                client_socket.send(audio_value.to_bytes(2, "little"))

        except:
            print("Retrying in 1 second...")
            time.sleep(1)
            
if __name__ == "__main__":
    wifi_ssid = "DESKTOP"
    wifi_password = "00000000"
    connect_to_wifi(wifi_ssid, wifi_password)

    HOST = "0.0.0.0"  # Listen on all available interfaces
    PORT = 49152    # general purpose port numbers from 49152 to 65535
    
    _thread.start_new_thread(read_ADC,())
    send_adc_data(HOST, PORT)
    
