import logging
import pandas as pd
import os
from tqdm import tqdm

# Configure the logging
logging.basicConfig(
    filename='error.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s - module:%(module)s, function:%(funcName)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)


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


def validate_integers_with_logging(df, filename):
    for col in df.columns[1:]:
        for idx, value in enumerate(df[col]):
            try:
                int(value)
            except (ValueError, TypeError):
                logging.warning(
                    f"Invalid value '{value}' at row {idx}, column '{col}' in file '{filename}'"
                )


directory = "../DataSample"
target_string = "precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1"

files = [f for f in os.listdir(directory) if f.endswith(".dat")]
for filename in tqdm(files, desc="Processing files in directory"):
    filepath = os.path.join(directory, filename)

    if not string_exists_in_file(filepath, target_string):
        logging.info(f"The string '{target_string}' was not found in the file '{filepath}'.")

    try:
        df = pd.read_csv(filepath, skiprows=2, sep=r'\s+', engine='python', header=None)
    except Exception as e:
        logging.error(f"Error processing file with pandas {filename}: {e}")
        continue

    # Check the dimensions of the DataFrame. Logs an error if they don't match 1140 rows and 33 columns.
    check_file_dimensions(df, filename)

    # Validate integer values in the DataFrame.
    validate_integers_with_logging(df, filename)


