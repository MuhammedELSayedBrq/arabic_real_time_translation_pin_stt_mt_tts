import threading
import streamlit as st
import time

start_button_c = st.button('Start receiving')
chu = st.button('chunk')

def print_numbers():
    while True:
        print(f"hello")
        st.text('hello')
        time.sleep(0.5)

if start_button_c:
    thread1 = threading.Thread(target=print_numbers())
    thread1.start()

if __name__ == '__main__':
    while True:
        print("normal_thread.")
        st.text('normal_thread')
        time.sleep(0.9)
