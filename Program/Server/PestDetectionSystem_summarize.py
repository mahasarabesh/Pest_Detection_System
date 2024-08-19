"""
    This programs is Designed and Tested to run on a PC that can run Python.
    Before Running this program make sure:
         i)all the neccesary Libraries are installed.
        ii)pest_data.csv file is available
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#loading the CSV file
df = pd.read_csv('pest_data.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True)

#Temperature, Humidity vs Time
plt.figure(figsize=(12, 6))
plt.title('Temperature and Humidity Over Time')
plt.plot(df.index, df['Temperature (C)'], label='Temperature (C)', color='orange')
plt.plot(df.index, df['Humidity (%)'], label='Humidity (%)', color='blue')
plt.xlabel('Time')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#Plot to visualize the Count of each pest detected
plt.figure(figsize=(10, 5))
plt.title('Detected Pest Count')
sns.countplot(data=df, x='Pest', palette='viridis')
plt.xlabel('Pest Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Temperature Distribution
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.title('Temperature Distribution')
sns.histplot(df['Temperature (C)'], kde=True, color='orange')
plt.xlabel('Temperature (C)')

#Humidity Distribution
plt.subplot(1, 2, 2)
plt.title('Humidity Distribution')
sns.histplot(df['Humidity (%)'], kde=True, color='blue')
plt.xlabel('Humidity (%)')
plt.tight_layout()
plt.show()

#Correlation Heatmap of the DataFrame
plt.figure(figsize=(8, 5))
plt.title('Correlation Heatmap')
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.tight_layout()
plt.show()
