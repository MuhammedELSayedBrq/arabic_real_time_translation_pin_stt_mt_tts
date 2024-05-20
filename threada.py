import threading
#import streamlit as st
import time

#start_button_c = st.button('Start receiving')
#chu = st.button('chunk')

def stop_thread(thread):
    def _async_raise(tid, exctype):
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("Invalid thread ID")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    if not thread.is_alive():
        return

    tid = thread.ident
    _async_raise(tid, SystemExit)

def print_numbers():
    while True:
        print(f"hello")
 #       st.text('hello')
        time.sleep(0.5)
"""
if start_button_c:
    thread1 = threading.Thread(target=print_numbers())
    thread1.start()
"""
if __name__ == '__main__':
    while True:
        print("normal_thread.")
  #      st.text('normal_thread')
        time.sleep(0.9)
