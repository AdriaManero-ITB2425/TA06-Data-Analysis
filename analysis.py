import pandas as pd
import numpy as np

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

#Dataframe 1

#Leer el Dataframe
df = pd.read_csv('./DataSample/precip.P8.MIROC5.RCP60.2006-2100.REGRESION.dat', sep='\s+', header=None, skiprows=2)
#Crear los nombres de los headers
column_name = ['ID', 'YEAR', 'MONTH'] + [f'D{i}' for i in range(1, 32)]

#Introducir los headers
df.columns = column_name

#Reemplazar los valores -999 por NA
df.replace(-999, pd.NA, inplace=True)

#Mostrar total de valores y valores nulos
print(df.size)
print(df.isnull().sum().sum())


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
total_precip = df_melted.groupby('YEAR')['VALUE'].sum() / 10


#Combrovar que si un año es bisiesto se le añade un dia
for year in total_valid_days.index:
    if is_leap_year(year):
        total_valid_days.loc[year] += 1

#Calcular la media de precipitacion por año
print(total_valid_days)
print(total_precip)

mean = total_precip / total_valid_days

print(mean)

# Juntar los dos dataframes
combined_df = pd.concat([mean.rename('Mean'), total_precip.rename('TotalPrecip')], axis=1)

print(combined_df)


#Dataframe 2

#Leer el Dataframe
df2 = pd.read_csv('./DataSample/precip.P16.MIROC5.RCP60.2006-2100.REGRESION.dat', sep='\s+', header=None, skiprows=2)
#Crear los nombres de los headers
column_name = ['ID', 'YEAR', 'MONTH'] + [f'D{i}' for i in range(1, 32)]

#Introducir los headers
df2.columns = column_name

#Reemplazar los valores -999 por NA
df2.replace(-999, pd.NA, inplace=True)

#Mostrar total de valores y valores nulos
print(df2.size)
print(df2.isnull().sum().sum())


#Cambiar el formato del DF a long format
df_melted2 = df2.melt(id_vars=['ID', 'YEAR', 'MONTH'], var_name='DAY', value_name='VALUE')
#Ordenar los valores por año y mes
df_melted2 = df_melted2.sort_values(by=['YEAR', 'MONTH'])

#Contar el total de dias sin valores (null) (por año)
total_null_days2 = df_melted2.groupby('YEAR')['VALUE'].apply(lambda x: x.isna().sum())

#Contar el total de dias (por año)
total_count_days2 = df_melted2.groupby('YEAR')['VALUE'].count()

#Calcular el total de dias validos (con datos para hacer la divison luego) (por año)
total_valid_days2 = total_count_days2 - total_null_days2
#calcular la precipitacion total por año i pasarla a metros por litro cuadrado (mm -> m^3)
total_precip2 = df_melted2.groupby('YEAR')['VALUE'].sum() / 10


#Combrovar que si un año es bisiesto se le añade un dia
for year in total_valid_days.index:
    if is_leap_year(year):
        total_valid_days.loc[year] += 1

#Calcular la media de precipitacion por año
print(total_valid_days2)
print(total_precip2)

mean2 = total_precip2 / total_valid_days2

print(mean2)

# Juntar los dos dataframes
combined_df2 = pd.concat([mean2.rename('Mean'), total_precip2.rename('TotalPrecip')], axis=1)

print(combined_df)
print(combined_df2)

#New df
total_df = combined_df + combined_df2
total_df = total_df / 2
print(total_df)