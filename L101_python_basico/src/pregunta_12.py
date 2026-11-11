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


def sum_metrics(text):
    """Add up the numeric values of a text like 'aaa:1,bbb:2'."""
    total = 0

    for item in text.split(","):
        value = item.split(":")[1]
        total = total + int(value)

    return total


def sum_metrics_by_letter(rows):
    """Add up the metrics values of the fifth column for each letter."""
    sums = {}

    for row in rows:
        letter = row[0]
        total = sum_metrics(row[4])

        if letter in sums:
            sums[letter] = sums[letter] + total
        else:
            sums[letter] = total

    return sums


def sort_sums(sums):
    """Return a new dictionary with the letters in alphabetical order."""
    result = {}

    for letter in sorted(sums):
        result[letter] = sums[letter]

    return result


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """
    rows = read_rows(INPUT_FILE)
    sums = sum_metrics_by_letter(rows)
    return sort_sums(sums)