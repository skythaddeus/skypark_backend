import pickle
import time
import threading
import requests
from PIL import Image
import io
import base64

def encode_image_to_base64(image_path):
    # Open the image with Pillow
    with Image.open(image_path) as img:
        # Save the image to a bytes buffer
        img = img.resize((img.width // 2, img.height // 2))
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")  # Choose PNG or the format of your choice
        # Encode the image bytes to base64
        base64_encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return base64_encoded

def my_function():
    with open('CarParkStatus', 'rb') as f:
        status = pickle.load(f)

    status["parking_space"] = "SKYPARK"
    status["img"] = encode_image_to_base64('captured_image.jpg')

    url = 'http://10.10.49.224:3000/api/parking-slot'
    data = {'data': status}

    # x = requests.post(url, json=data)
    # print(x.text)
    print(data)

def run_every_10_seconds():
    while True:
        my_function()
        time.sleep(5)  # Wait for 10 seconds

# Start the function in a separate thread
thread = threading.Thread(target=run_every_10_seconds)
thread.start()
