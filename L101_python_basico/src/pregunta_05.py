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


def max_min_by_letter(rows):
    """Find the maximum and minimum value of the second column for each letter."""
    limits = {}

    for row in rows:
        letter = row[0]
        value = int(row[1])

        if letter in limits:
            current_max, current_min = limits[letter]
            limits[letter] = (max(current_max, value), min(current_min, value))
        else:
            limits[letter] = (value, value)

    return limits


def sort_limits(limits):
    """Return the limits as a list of (letter, max, min) tuples sorted by letter."""
    result = []

    for letter in sorted(limits):
        maximum, minimum = limits[letter]
        result.append((letter, maximum, minimum))

    return result


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    rows = read_rows(INPUT_FILE)
    limits = max_min_by_letter(rows)
    return sort_limits(limits)
