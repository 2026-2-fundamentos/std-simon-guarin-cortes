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


def parse_codes(text):
    """Convert a text like 'a,b,c' into a list of letters."""
    codes = []

    for item in text.split(","):
        codes.append(item.strip())

    return codes


def sum_by_code(rows):
    """Add up the values of the second column for each letter in the fourth column."""
    sums = {}

    for row in rows:
        value = int(row[1])

        for code in parse_codes(row[3]):
            if code in sums:
                sums[code] = sums[code] + value
            else:
                sums[code] = value

    return sums


def sort_sums(sums):
    """Return a new dictionary with the letters in alphabetical order."""
    result = {}

    for code in sorted(sums):
        result[code] = sums[code]

    return result


def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """
    rows = read_rows(INPUT_FILE)
    sums = sum_by_code(rows)
    return sort_sums(sums)