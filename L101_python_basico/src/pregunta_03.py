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


def sum_by_letter(rows):
    """Add up the values of the second column for each letter."""
    sums = {}

    for row in rows:
        letter = row[0]
        value = int(row[1])

        if letter in sums:
            sums[letter] = sums[letter] + value
        else:
            sums[letter] = value

    return sums


def sort_sums(sums):
    """Return the sums as a list of (letter, sum) tuples sorted by letter."""
    result = []

    for letter in sorted(sums):
        result.append((letter, sums[letter]))

    return result


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """
    rows = read_rows(INPUT_FILE)
    sums = sum_by_letter(rows)
    return sort_sums(sums)