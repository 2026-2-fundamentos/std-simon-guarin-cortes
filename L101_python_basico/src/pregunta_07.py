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


def letters_by_value(rows):
    """Group the letters of the first column by the value of the second column."""
    groups = {}

    for row in rows:
        letter = row[0]
        value = int(row[1])

        if value in groups:
            groups[value].append(letter)
        else:
            groups[value] = [letter]

    return groups


def sort_groups(groups):
    """Return the groups as a list of (value, letters) tuples sorted by value."""
    result = []

    for value in sorted(groups):
        result.append((value, groups[value]))

    return result


def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """
    rows = read_rows(INPUT_FILE)
    groups = letters_by_value(rows)
    return sort_groups(groups)