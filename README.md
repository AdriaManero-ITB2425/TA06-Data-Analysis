# TA06-Data-Analysis
Data analysis with Python


In the face of urgent challenges such as climate change, loss of biodiversity,  resource constraints, emerging micropollutants or waste of water. For instance,  cities need to improve or reinvent urban services.

It is compulsory to design and deploy innovative solutions and unique technologies for managing water, waste and energy.

The objective of this task, is to use the power of data and the most advanced AI technologies trained with “our expertise”, to tailor solutions in the green transformation, be it decarbonization, decontamination, resource saving and regeneration, or any other solution.

It is for this reason that we set ourselves the challenge of processing the data that the  AEMET “Agéncia Estatal de Meteorología” publishes on the web OpenData AEMET

# Table of contents

1. Obtencion de datos
2. Organicacion y procesamiento de datos
3. Analisis de datos y visualizacion
4. Publicacion de datos
5. Reflexion
6. Referencias


# 1. Obtencion de datos

Para realizar esta tarea es necesario obtener los datos de una fuente fiable de meteorologia, en este caso se ha optado por la AEMET, la Agencia Estatal de Meteorología de España.

La AEMET pone a disposición de los usuarios una API para la obtención de datos meteorológicos, en este caso se ha optado por la API de datos abiertos de la AEMET, que se puede consultar en la siguiente dirección: https://opendata.aemet.es/centrodedescargas/altaUsuario

Una vez obtenida la API Key, nos podemos dirigir a la siguiente dirección para obtener los datos que deeseemos: https://www.aemet.es/es/serviciosclimaticos/cambio_climat/datos_diarios

En este caso se ha optado por obtener los datos con las siguientes características:

Metodo: Regresion rejilla
Modelo: MIROC5
Escenario: RCP 6.0
Variable: Precipitación
Periodo: 2006-2100

En este link podeis descargar el fichero con los datos: https://www.aemet.es/documentos_d/serviciosclimaticos/cambio_climat/datos_diarios/reg_e/ar5/sdsm_rej/MIROC5/RCP60/precip.MIROC5.RCP60.2006-2100.SDSM_REJ.tar.gz
https://www.aemet.es/documentos_d/serviciosclimaticos/cambio_climat/datos_diarios/reg_e/ar5/sdsm_rej/MIROC5/RCP60/precip.MIROC5.RCP60.2006-2100.SDSM_REJ.tar.gz

# 2. Organizacion y procesamiento de datos

Una vez descargado el fichero, lo descomprimimos y obtenemos los ficheros con los datos de precipitación.

````csv
precip	MIROC5	RCP60	REGRESION	decimas	1
P1	35.307	-2.948	182	geo	2006	2100	-1
P1 2006 1 0 0 0 24 21 20 0 0 0 0 0 20 35 37 18 0 0 0 13 14 0 0 0 0 0 0 0 0 14 0 0 
P1 2006 2 0 0 0 13 0 0 0 0 2 0 0 0 0 0 31 0 0 0 0 0 23 25 21 26 0 0 0 0 -999 -999 -999 
P1 2006 3 0 0 11 0 0 16 20 24 0 0 39 38 23 0 0 19 17 0 12 0 0 0 0 0 16 0 0 7 0 15 20 
P1 2006 4 9 0 0 0 0 7 0 0 0 15 6 0 0 0 0 0 0 0 14 0 0 0 0 0 0 15 23 0 0 19 -999 
P1 2006 5 0 14 15 16 0 0 11 0 0 0 0 0 0 0 0 0 0 0 10 6 0 0 0 0 0 0 0 0 0 0 0 
P1 2006 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 7 0 0 0 0 -999 
P1 2006 7 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 
P1 2006 8 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 4 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 
P1 2006 9 0 5 0 0 0 0 0 0 0 0 5 0 0 4 0 0 0 0 0 0 0 0 0 9 0 0 6 0 0 0 -999 
````

Esto es un ejemplo de los datos que se pueden encontrar en el fichero, si nos fijamos, la primera fila nos indica el tipo de datos que contiene el fichero, en este caso precipitación, modelo MIROC5, escenario RCP60, método de regresión y decimas.
La segunda fila nos indica la longitud y latitud de la localización, el año de inicio y fin de los datos y el valor de la decima.
La primera columna nos indica el ID de la estacion, en este caso P1, la segunda columna nos indica el año, la tercera columna nos indica el mes y las siguientes columnas nos indican los valores de precipitación para cada día del mes.

Teoricamente todos los ficheros deberian tener la misma estructura, pero es necesario validar que los datos sean correctos y no haya datos nulos.

Cada fichero debe tener siempre la primera linea identica. 

Todos los fichero deberinan tener 1140 lineas (12 meses * 95 años) + 2 lineas de cabecera, y 34 columnas. (ID de la estacion, año, mes y 31 dias)

Todos los ficheros deberian tener datos de tipo INT, excluyendo la primera columna y las dos primeras filas de cabecera.

Sabiendo esto, hemos creado un script en python para validar estas 3 condiciones.

Antes de procesar los datos y generar resultados y estadísticas, es necesario validar-los para su posterior análisis.

Para ello, hemos creado un script en Python que valida que la estructura de los datos sea correcta y que no haya datos nulos.

task_02/Data_Validation.py

Breakdown del script:


```python
def string_exists_in_file(filepath, target_string):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return any(target_string in line for line in file)
    except FileNotFoundError:
        logging.error(f"The file '{filepath}' was not found.")
    except PermissionError:
        logging.error(f"Permission denied to read the file '{filepath}'.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return False
```
Esta primera funcion nos permite comprobar si un string se encuentra en un fichero, en este caso lo utilizamos para comprobar si la primera linea del fichero es correcta.

```python
def check_file_dimensions(df, filename):
    """
    Checks if the DataFrame has 1140 rows and 33 columns.
    If dimensions differ, logs an error with the actual dimensions.
    """
    rows, cols = df.shape
    if rows != 1140 or cols != 34:
        logging.error(
            f"Dimension mismatch in file '{filename}': Found {rows} rows and {cols} columns, "
            "expected 1140 rows and 33 columns."
        )
```
Esta segunda funcion nos permite comprobar si el fichero tiene las dimensiones correctas, en este caso 1140 filas y 34 columnas.

```python
def validate_integers_with_logging(df, filename):
    for col in df.columns[1:]:
        for idx, value in enumerate(df[col]):
            try:
                int(value)
            except (ValueError, TypeError):
                logging.warning(
                    f"Invalid value '{value}' at row {idx}, column '{col}' in file '{filename}'"
                )
```

Esta tercera funcion nos permite comprobar si los valores del fichero son de tipo INT, en caso de que no lo sean, se muestra un warning.


Una vez hemos validado los datos, podemos procesarlos y generar estadisticas.

# 3. Analisis de datos y visualizacion