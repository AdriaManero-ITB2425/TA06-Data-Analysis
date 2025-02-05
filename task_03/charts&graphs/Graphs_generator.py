import pandas as pd
import matplotlib.pyplot as plt

df_results = pd.read_csv('.././data_analysis/mean_output_with_stats.csv')
df_top5dry = df_results.nsmallest(5, columns='TotalPrecip')
df_top5wet = df_results.nlargest(5, columns='TotalPrecip')

# Visualize the data
plt.figure(figsize=(10, 6))
plt.bar(df_results.index, df_results['TotalPrecip'], label='Total Precipitation', color='b')
plt.bar(df_results.index, df_results['Mean'], label='Mean Precipitation', color='g')
plt.xlabel('Year')
plt.ylabel('Precipitation (l/m²)')
plt.title('Total and Mean Precipitation Over Years')
plt.legend()
plt.grid(True)
plt.savefig("my_plot1.png", dpi=300, bbox_inches='tight')
plt.show()

# Visualize top 5 driest and wettest years in a single graph with different colors
fig, ax = plt.subplots(figsize=(10, 6))

years = list(df_top5dry.index) + list(df_top5wet.index)
values = list(df_top5dry['TotalPrecip']) + list(df_top5wet['TotalPrecip'])
colors = ['brown'] * len(df_top5dry) + ['blue'] * len(df_top5wet)

ax.bar(years, values, color=colors)
ax.set_title('Top 5 Driest and Wettest Years')
ax.set_xlabel('Year')
ax.set_ylabel('Total Precipitation (l/m²)')

plt.tight_layout()
plt.savefig("my_plot2.png", dpi=300, bbox_inches='tight')
plt.show()

# Visualize the percentage change of the df_results DataFrame
plt.figure(figsize=(10, 6))
plt.plot(df_results.index, df_results['PctChange'], label='Percentage Change', color='r')
plt.xlabel('Year')
plt.ylabel('Percentage Change (%)')
plt.title('Percentage Change of Total Precipitation Over Years')
plt.legend()
plt.grid(True)
plt.savefig("my_plot3.png", dpi=300, bbox_inches='tight')
plt.show()

# Save data to JSON files
df_results.to_json('mean_results.json')
df_top5dry.to_json('top_5_driest.json')
df_top5wet.to_json('top_5_wettest.json')


