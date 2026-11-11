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


def parse_metrics(text):
    """Convert a text like 'aaa:1,bbb:2' into a list of (key, value) pairs."""
    pairs = []

    for item in text.split(","):
        key, value = item.split(":")
        pairs.append((key.strip(), int(value)))

    return pairs


def min_max_by_key(rows):
    """Find the minimum and maximum value for each key in the fifth column."""
    limits = {}

    for row in rows:
        for key, value in parse_metrics(row[4]):
            if key in limits:
                current_min, current_max = limits[key]
                limits[key] = (min(current_min, value), max(current_max, value))
            else:
                limits[key] = (value, value)

    return limits


def sort_limits(limits):
    """Return the limits as a list of (key, min, max) tuples sorted by key."""
    result = []

    for key in sorted(limits):
        minimum, maximum = limits[key]
        result.append((key, minimum, maximum))

    return result


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    rows = read_rows(INPUT_FILE)
    limits = min_max_by_key(rows)
    return sort_limits(limits)
