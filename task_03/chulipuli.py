import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
data = pd.read_csv('mean_output_with_stats.csv')

# Plot the bar graph of the total precipitation over the years
plt.figure(figsize=(20, 20))
plt.bar(data['Year'], data['TotalPrecip'], color='blue', edgecolor='black')
plt.title('Total Precipitation Over the Years')
plt.xlabel('Year')
plt.ylabel('Total Precipitation (mm)')
plt.grid(True)
plt.show()