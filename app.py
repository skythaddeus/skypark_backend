import pickle
import time
import threading

def my_function():
    with open('CarParkStatus', 'rb') as f:
        status = pickle.load(f)

    print(status)

def run_every_10_seconds():
    while True:
        my_function()
        time.sleep(5)  # Wait for 10 seconds

# Start the function in a separate thread
thread = threading.Thread(target=run_every_10_seconds)
thread.start()
