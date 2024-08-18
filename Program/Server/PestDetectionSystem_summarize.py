import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('pest_data.csv')

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True)

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


plt.figure(figsize=(10, 5))
plt.title('Detected Pest Count')
sns.countplot(data=df, x='Pest', palette='viridis')
plt.xlabel('Pest Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.title('Temperature Distribution')
sns.histplot(df['Temperature (C)'], kde=True, color='orange')
plt.xlabel('Temperature (C)')


plt.subplot(1, 2, 2)
plt.title('Humidity Distribution')
sns.histplot(df['Humidity (%)'], kde=True, color='blue')
plt.xlabel('Humidity (%)')
plt.tight_layout()
plt.show()


plt.figure(figsize=(8, 5))
plt.title('Correlation Heatmap')
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.tight_layout()
plt.show()
