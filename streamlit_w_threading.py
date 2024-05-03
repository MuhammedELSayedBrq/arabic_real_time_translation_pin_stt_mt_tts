import threading
import streamlit as st
import time

def long():
    for i in range(10):
        time.sleep(1)
        st.write('task')
    st.success('done')

def short():
    for i in range(10,20):
        time.sleep(1)
        st.write('task2')
    st.success('done')

def main():
    if st.button('run'):
        task_th = threading.Thread(target=long())
        task_sh = threading.Thread(target=short())
        task_th.start()
        task_sh.start()


if __name__ == '__main__':
    main()