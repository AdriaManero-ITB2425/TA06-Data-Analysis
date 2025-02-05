import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import logging

#Ruta de la carpeta de los datos

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


Folder_path = './DataSample'
column_name = ['ID', 'YEAR', 'MONTH'] + [f'D{i}' for i in range(1, 32)]
#Inicializar un DataFrame para almacenar los resultados agregados

aggregated_results = pd.DataFrame()

#Obtener la lista de archivos en la carpeta

lista_archivos = [file for file in os.listdir(Folder_path) if os.path.isfile(os.path.join(Folder_path, file))]

#Contador de archivos procesados

file_count = 0
total_valores_procesados = 0
total_valores_nulos_procesados = 0

#Iterar sobre todos los archivos en la carpeta con una barra de progreso

for file_name in tqdm(lista_archivos, desc='Procesando archivos', unit='archivo'):
    file_path = os.path.join(Folder_path, file_name)

    try:
        #Leer el archivo CSV omitiendo las primeras dos filas
        df = pd.read_csv(file_path, skiprows=2, sep=r'\s+', engine='python', header=None)

        #Crear los nombres de los headers
        df.columns = column_name

        df.replace(-999, pd.NA, inplace=True)

        #Mostrar total de valores y valores nulos
        total_valores_procesados += df.size
        total_valores_nulos_procesados += df.isnull().sum().sum()

        #Cambiar el formato del DF a long format
        df_melted = df.melt(id_vars=['ID', 'YEAR', 'MONTH'], var_name='DAY', value_name='VALUE')
        #Ordenar los valores por año y mes
        df_melted = df_melted.sort_values(by=['YEAR', 'MONTH'])


        #Contar el total de dias sin valores (null) (por año)
        total_null_days = df_melted.groupby('YEAR')['VALUE'].apply(lambda x: x.isna().sum())

        #Contar el total de dias (por año)
        total_count_days = df_melted.groupby('YEAR')['VALUE'].count()

        #Calcular el total de dias validos (con datos para hacer la divison luego) (por año)
        total_valid_days = total_count_days - total_null_days
        #calcular la precipitacion total por año i pasarla a metros por litro cuadrado (mm -> m^3)
        df_total_precip= df_melted.groupby('YEAR')['VALUE'].sum() / 10

        #Combrovar que si un año es bisiesto se le añade un dia
        for year in total_valid_days.index:
            if is_leap_year(year):
                total_valid_days.loc[year] += 1

        #Calcular la media de precipitacion por año
        df_with_mean = df_total_precip/ total_valid_days

        # Juntar los dos dataframes
        combined_df = pd.concat([df_with_mean.rename('Mean'), df_total_precip.rename('TotalPrecip')], axis=1)

        #Agregar los resultados al DataFrame agregado

        if aggregated_results.empty:
            aggregated_results = combined_df
        else:
            aggregated_results = aggregated_results.add(combined_df, fill_value=None)

        file_count +=1

    except Exception as e:
        print(f'Error processing file {file_name}: {e}')

#Calcular la media de los valores agregados

mean_results = aggregated_results / file_count

print(aggregated_results)

print(mean_results)

