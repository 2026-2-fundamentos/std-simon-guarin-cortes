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


def count_by_month(rows):
    """Count how many records there are for each month in the third column."""
    counts = {}

    for row in rows:
        date = row[2]
        month = date.split("-")[1]

        if month in counts:
            counts[month] = counts[month] + 1
        else:
            counts[month] = 1

    return counts


def sort_counts(counts):
    """Return the counts as a list of (month, count) tuples sorted by month."""
    result = []

    for month in sorted(counts):
        result.append((month, counts[month]))

    return result


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    rows = read_rows(INPUT_FILE)
    counts = count_by_month(rows)
    return sort_counts(counts)