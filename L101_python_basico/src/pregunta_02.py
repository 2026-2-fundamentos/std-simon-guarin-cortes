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


def count_letters(rows):
    """Count how many records there are for each letter in the first column."""
    counts = {}

    for row in rows:
        letter = row[0]

        if letter in counts:
            counts[letter] = counts[letter] + 1
        else:
            counts[letter] = 1

    return counts


def sort_counts(counts):
    """Return the counts as a list of (letter, count) tuples sorted by letter."""
    result = []

    for letter in sorted(counts):
        result.append((letter, counts[letter]))

    return result


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    rows = read_rows(INPUT_FILE)
    counts = count_letters(rows)
    return sort_counts(counts)