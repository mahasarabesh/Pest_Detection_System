import requests
import json
import tkinter as tk
from tkinter import ttk
import time
import os
import pandas as pd
from datetime import datetime

class PestDetectionDisplay:
    def __init__(self, channel_id, read_api_key, save_interval=600, filename="pest_data.csv"):
        self.channel_id = channel_id
        self.read_api_key = read_api_key
        self.filename = filename
        self.save_interval = save_interval

        if os.path.exists('pest_data.csv'):
            self.dataframe=pd.read_csv('pest_data.csv',index_col='Timestamp')
        else:
            self.dataframe = pd.DataFrame(columns=['Timestamp', 'Pest', 'Temperature (C)', 'Humidity (%)'])

        self.root = tk.Tk()
        self.root.title("Pest Detection System Data Display")
        self.temp_label = tk.Label(self.root, text="Temperature: -- C", font=("Arial", 14))
        self.temp_label.pack(pady=10)
        self.humid_label = tk.Label(self.root, text="Humidity: -- %", font=("Arial", 14))
        self.humid_label.pack(pady=10)
        self.result_label = tk.Label(self.root, text="Detected Pest: None", font=("Arial", 14))
        self.result_label.pack(pady=10)
        self.update_button = tk.Button(self.root, text="Update Data", command=self.update_data, font=("Arial", 14))
        self.update_button.pack(pady=10)
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, font=("Arial", 14))
        self.quit_button.pack(pady=10)

        self.update_data()
        self.root.after(self.save_interval * 1000, self.update_data)

    def fetch_data(self):
        url = f'https://api.thingspeak.com/channels/{self.channel_id}/feeds.json?api_key={self.read_api_key}&results=1'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                if data['feeds']:
                    latest_feed = data['feeds'][0]
                    temp = latest_feed['field1']
                    humid = latest_feed['field2']
                    pest_index = latest_feed['field3']
                    return temp, humid, pest_index
                else:
                    return None, None, None
            else:
                return None, None, None
        except requests.RequestException as e:
            print(f"Failed to fetch data: {e}")
            return None, None, None

    def update_data(self):
        temp, humid, pest_index = self.fetch_data()
        if temp and humid and pest_index:
            self.temp_label.config(text=f"Temperature: {temp} C")
            self.humid_label.config(text=f"Humidity: {humid} %")
            pest_name = self.get_pest_name(int(pest_index))
            self.result_label.config(text=f"Detected Pest: {pest_name}")
            self.update_dataframe(pest_name, temp, humid)

        else:
            self.temp_label.config(text="Temperature: -- C")
            self.humid_label.config(text="Humidity: -- %")
            self.result_label.config(text="Detected Pest: None")

    def get_pest_name(self, index):
        result_names = ["ants", "aphids", "armyworm", "bees","beetle","bollworm","catterpillar","earthworms","earwig","grasshopper","mites","mosquito","moth","sawfly","slug","snail","stem_borer","wasp","weevil"]  # Example names
        if 0 <= index < len(result_names):
            return result_names[index]
        else:
            return "Unknown"

    def update_dataframe(self, pest, temp, humid):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {'Timestamp': timestamp, 'Pest': pest, 'Temperature (C)': temp, 'Humidity (%)': humid}
        self.dataframe = self.dataframe.append(data, ignore_index=True)
        self.save_dataframe()

    def save_dataframe(self):
        try:
            self.dataframe.to_csv(self.filename, index=False)
            print(f"Data saved to {self.filename}")
        except Exception as e:
            print(f"Failed to save data: {e}")

    def periodic_save(self):
        self.save_dataframe()
        self.root.after(self.save_interval * 1000, self.periodic_save)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    display = PestDetectionDisplay(
        channel_id='YourChannelId',
        read_api_key='YourReadAPIKey',
        save_interval=600,
        filename="pest_data.csv"
    )
    display.run()
