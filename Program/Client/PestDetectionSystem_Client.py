import time
import adafruit_dht
import board
import requests
import numpy as np
import tensorflow as tf
from PIL import Image
import cv2
import pickle as pk
from picamera import PiCamera

class PestDetectionSystem:
    def __init__(self, model_path, result_names_path, channel_id, write_api_key, dht_pin=board.D26):
        self.camera = PiCamera()
        self.channel_id = channel_id
        self.write_api_key = write_api_key
        self.dht_device = adafruit_dht.DHT11(dht_pin)
        

        with open(result_names_path, 'rb') as f:
            self.result_names = pk.load(f)
        

        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_type = self.input_details[0]['dtype']
        self.input_shape = self.input_details[0]['shape']
        self.size = (self.input_shape[1], self.input_shape[2])
        print('Initialization complete.')

    def capture_image(self, image_path='test.jpg'):
        self.camera.start_preview()
        self.camera.annotate_text = "Hello!!"
        time.sleep(5)
        self.camera.capture(image_path)
        self.camera.stop_preview()
        return image_path

    def process_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize(self.size)
        
        input_data = np.array(image, dtype=np.float32)
        input_data = np.expand_dims(input_data, axis=0)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        self.interpreter.invoke()
        prediction = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        return self.get_prediction_result(prediction)

    def get_prediction_result(self, prediction):
        result_index = np.argmax(prediction[0])
        print(self.result_names[result_index])
        return result_index

    def read_sensor_data(self):
        temperature_c = self.dht_device.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = self.dht_device.humidity
        print(f"Temp: {temperature_c:.1f} C / {temperature_f:.1f} F    Humidity: {humidity}%")
        return temperature_c, humidity

    def send_data(self, temp, humid, index):
        data = {'Temperature': temp, 'Humidity': humid}
        update_url = f'https://api.thingspeak.com/update?api_key={self.write_api_key}&field1={temp}&field2={humid}&field3={index}'
        
        try:
            response = requests.post(update_url, data=data)
            if response.status_code == 200:
                print(f'Data updated successfully: {data}')
        except requests.RequestException as e:
            print(f'Request failed: {e}')

    def run(self, interval=20.0):
        while True:
            try:
                image_path = self.capture_image()
                index = self.process_image(image_path)
                temp, humid = self.read_sensor_data()
                self.send_data(temp, humid, index)
            except RuntimeError as err:
                print(err.args[0])
            time.sleep(interval)

    def close(self):
        self.camera.close()


if __name__ == "__main__":
    system = PestDetectionSystem(
        model_path="model_1.tflite",
        result_names_path="result_names.pkl",
        channel_id='YourChannelId',
        write_api_key='YourWriteAPIKey'
    )
    
    try:
        system.run()
    except KeyboardInterrupt:
        print("Terminating the system...")
    finally:
        system.close()
