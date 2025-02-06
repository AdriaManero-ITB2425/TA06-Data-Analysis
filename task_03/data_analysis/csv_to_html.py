import pandas as pd

df = pd.read_csv('mean_output_with_stats.csv')

html = df.to_html('html_output.html')
