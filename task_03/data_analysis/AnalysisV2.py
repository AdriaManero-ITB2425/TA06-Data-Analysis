import os
import pandas as pd
from tqdm import tqdm
import logging
from colorama import Fore, Style, init
import matplotlib.pyplot as plt


# Initialize colorama
init(autoreset=True)

logging.basicConfig(
    filename='error.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s - module:%(module)s, function:%(funcName)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

pd.set_option('future.no_silent_downcasting', True)

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Ruta de la carpeta de los datos
Folder_path = '../../precip.MIROC5.RCP60.2006-2100.SDSM_REJ'
column_name = ['ID', 'YEAR', 'MONTH'] + [f'D{i}' for i in range(1, 32)]
# Inicializar un DataFrame para almacenar los resultados agregados
aggregated_results = pd.DataFrame()

# Obtener la lista de archivos en la carpeta
lista_archivos = [file for file in os.listdir(Folder_path) if os.path.isfile(os.path.join(Folder_path, file))]

# Contador de archivos procesados
file_count = 0
total_valores_procesados = 0
total_valores_nulos_procesados = 0

# Iterar sobre todos los archivos en la carpeta con una barra de progreso
for file_name in tqdm(lista_archivos, desc='Procesando archivos', unit='it'):
    file_path = os.path.join(Folder_path, file_name)

    try:
        # Leer el archivo CSV omitiendo las primeras dos filas
        df = pd.read_csv(file_path, skiprows=2, sep=r'\s+', engine='python', header=None)

        # Crear los nombres de los headers
        df.columns = column_name

        df.replace(-999, pd.NA, inplace=True)

        # Mostrar total de valores y valores nulos
        total_valores_procesados += df.size
        total_valores_nulos_procesados += df.isnull().sum().sum()

        # Cambiar el formato del DF a long format
        df_melted = df.melt(id_vars=['ID', 'YEAR', 'MONTH'], var_name='DAY', value_name='VALUE')
        # Ordenar los valores por año y mes
        df_melted = df_melted.sort_values(by=['YEAR', 'MONTH'])

        # Contar el total de dias sin valores (null) (por año)
        total_null_days = df_melted.groupby('YEAR')['VALUE'].apply(lambda x: x.isna().sum())

        # Contar el total de dias (por año)
        total_count_days = df_melted.groupby('YEAR')['VALUE'].count()

        # Calcular el total de dias validos (con datos para hacer la divison luego) (por año)
        total_valid_days = total_count_days - total_null_days
        # calcular la precipitacion total por año i pasarla a metros por litro cuadrado (mm -> m^3)
        df_total_precip = df_melted.groupby('YEAR')['VALUE'].sum() / 10

        # Combrovar que si un año es bisiesto se le añade un dia
        for year in total_valid_days.index:
            if is_leap_year(year):
                total_valid_days.loc[year] += 1

        # Calcular la media de precipitacion por año
        df_with_mean = df_total_precip / total_valid_days

        # Juntar los dos dataframes
        combined_df = pd.concat([df_with_mean.rename('Mean'), df_total_precip.rename('TotalPrecip')], axis=1)

        # Agregar los resultados al DataFrame agregado
        if aggregated_results.empty:
            aggregated_results = combined_df
        else:
            aggregated_results = aggregated_results.add(combined_df, fill_value=None)

        file_count += 1

    except Exception as e:
        logging.error(f'Error processing file {file_name}: {e}')


aggregated_results['Mean'] = aggregated_results['Mean'].astype(int)

# Calcular la media de los valores agregados
mean_results = aggregated_results / file_count

# Ensure 'TotalPrecip' is in mean_results
mean_results['TotalPrecip'] = aggregated_results['TotalPrecip'] / file_count

# Calculate the percentage change of the 'TotalPrecip' column
mean_results['PctChange'] = mean_results['TotalPrecip'].pct_change() * 100

pct_nulos = (total_valores_nulos_procesados / total_valores_procesados) * 100

# Guardar el DataFrame de resultados medios en un archivo CSV
mean_results.to_csv('mean_output_with_stats.csv', index=True)

# Convert 'TotalPrecip' to numeric
aggregated_results['TotalPrecip'] = pd.to_numeric(aggregated_results['TotalPrecip'])

# Calculate top 5 driest and wettest years
top_5_driest = aggregated_results.nsmallest(5, 'TotalPrecip') / file_count
top_5_wettest = aggregated_results.nlargest(5, 'TotalPrecip') /file_count

# Write the results to the data.log file
with open('data.log', 'w') as log_file:
    log_file.write("=========================================\n")
    log_file.write("=                                       =\n")
    log_file.write("=         DATA ANALYSIS RESULT          =\n")
    log_file.write("=                                       =\n")
    log_file.write("=========================================\n\n")
    log_file.write(f"Date: {pd.Timestamp.now()}\n\n")
    log_file.write("=========================================\n")
    log_file.write(f"Total of files processed: {file_count}\n")
    log_file.write(f"Total of values processed: {total_valores_procesados}\n")
    log_file.write(f"Total of null or empty values: {total_valores_nulos_procesados}\n")
    log_file.write(f"Percentage of null over total data: {pct_nulos:.2f}%\n")
    log_file.write("=========================================\n\n")
    log_file.write("===== Top 5 Driest Years =====\n")
    log_file.write("=========================================\n")
    for year, row in top_5_driest.iterrows():
        log_file.write(f"Year {year}: Total: {round(row['TotalPrecip'], 2)} l/m², Mean: {round(row['TotalPrecip'] / file_count, 2)} l/m²\n")
    log_file.write("=========================================\n\n")
    log_file.write("===== Top 5 Wettest Years =====\n")
    log_file.write("=========================================\n")
    for year, row in top_5_wettest.iterrows():
        log_file.write(f"Year {year}: Total: {round(row['TotalPrecip'], 2)} l/m², Mean: {round(row['TotalPrecip'] / file_count, 2)} l/m²\n")
    log_file.write("=========================================\n\n")
    log_file.write("===== Dataframe with total and mean =====\n")
    log_file.write("=========================================\n\n")
    for year, row in aggregated_results.iterrows():
        log_file.write(f"Year {year}: Total: {round(row['TotalPrecip'], 2)} l/m², Mean: {round(row['TotalPrecip'] / file_count, 2)} l/m²\n")

# Print the results to the terminal with colors
print(Fore.GREEN + "=========================================")
print(Fore.GREEN + "=                                       =")
print(Fore.GREEN + "=         DATA ANALYSIS RESULT          =")
print(Fore.GREEN + "=                                       =")
print(Fore.GREEN + "=========================================\n")
print(Fore.YELLOW + f"Date: {pd.Timestamp.now()}\n")
print(Fore.GREEN + "=========================================")
print(Fore.CYAN + f"Total of files processed: {file_count}")
print(Fore.CYAN + f"Total of values processed: {total_valores_procesados}")
print(Fore.CYAN + f"Total of null or empty values: {total_valores_nulos_procesados}")
print(Fore.CYAN + f"Percentage of null over total data: {pct_nulos:.2f}%")
print(Fore.GREEN + "=========================================\n")
print(Fore.GREEN + "===== Top 5 Driest Years =====")
print(Fore.GREEN + "=========================================")
for year, row in top_5_driest.iterrows():
    print(Fore.BLUE + f"Year {year}: Total: {round(row['TotalPrecip'], 2)} l/m², Mean: {round(row['TotalPrecip'] / file_count, 2)} l/m²")
print(Fore.GREEN + "=========================================\n")
print(Fore.GREEN + "===== Top 5 Wettest Years =====")
print(Fore.GREEN + "=========================================")
for year, row in top_5_wettest.iterrows():
    print(Fore.BLUE + f"Year {year}: Total: {round(row['TotalPrecip'], 2)} l/m², Mean: {round(row['TotalPrecip'] / file_count, 2)} l/m²")
print(Fore.GREEN + "=========================================\n")
print(Fore.GREEN + "===== Dataframe with total and mean =====")
print(Fore.GREEN + "=========================================\n")
for year, row in aggregated_results.iterrows():
    print(Fore.BLUE + f"Year {year}: Total: {round(row['TotalPrecip'], 2)} l/m², Mean: {round(row['TotalPrecip'] / file_count, 2)} l/m²")