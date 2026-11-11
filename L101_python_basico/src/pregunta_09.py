import csv
import gzip
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_FOLDER / "data" / "data.csv.gz"


def read_rows(input_file):
    """Read the compressed tab-separated file and return its data rows."""
    input_file = Path(input_file)

    with gzip.open(input_file, "rt", encoding="utf-8", newline="") as file:
        reader = csv.reader(file, delimiter="\t")
        rows = list(reader)

    # Skip the header if the second column is not a number
    if rows and not rows[0][1].lstrip("-").isdigit():
        rows = rows[1:]

    return rows


def parse_keys(text):
    """Extract the keys from a text like 'aaa:1,bbb:2'."""
    keys = []

    for item in text.split(","):
        key = item.split(":")[0]
        keys.append(key.strip())

    return keys


def count_keys(rows):
    """Count how many times each key appears in the fifth column."""
    counts = {}

    for row in rows:
        for key in parse_keys(row[4]):
            if key in counts:
                counts[key] = counts[key] + 1
            else:
                counts[key] = 1

    return counts


def sort_counts(counts):
    """Return a new dictionary with the keys in alphabetical order."""
    result = {}

    for key in sorted(counts):
        result[key] = counts[key]

    return result


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    rows = read_rows(INPUT_FILE)
    counts = count_keys(rows)
    return sort_counts(counts)