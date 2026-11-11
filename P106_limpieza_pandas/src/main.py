from pathlib import Path
import re
import pandas as pd

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ACTIVITY_DIR / "data" / "ventas.csv"
OUTPUT_FILE = ACTIVITY_DIR / "submission" / "ventas.csv"

SUPPLIER_REPLACEMENTS = {
    "amazon web services colombia": "Amazon Web Services Colombia",
    "BANCOLOMBIA S.A.": "Bancolombia S.A.",
    "Cementos Argos SA": "Cementos Argos S.A.",
    "cementos argos s.a.": "Cementos Argos S.A.",
    "Corona SAS": "Corona S.A.S.",
    "Ecopetrol  S.A.": "Ecopetrol S.A.",
    "GOOGLE COLOMBIA LTDA.": "Google Colombia Ltda.",
    "Grupo  Éxito  S.A.": "Grupo Éxito S.A.",
    "IBM Colombia SAS.": "IBM Colombia S.A.S.",
    "ibm colombia s.a.s.": "IBM Colombia S.A.S.",
    "MICROSOFT COLOMBIA INC.": "Microsoft Colombia Inc.",
    "Nutresa SA": "Nutresa S.A.",
    "nutresa s.a.": "Nutresa S.A.",
    "oracle colombia ltda.": "Oracle Colombia Ltda.",
    "POSTOBÓN S.A.": "Postobon S.A.",
    "SAP Colombia SAS": "SAP Colombia S.A.S.",
    "Schneider  Electric": "Schneider Electric",
    "SIEMENS S.A.S.": "Siemens S.A.S.",
    "siemens s.a.s.": "Siemens S.A.S.",
    "Sura  S.A.": "Sura S.A.",
    "Telefónica  Colombia": "Telefónica Colombia",
}


COUNTRY_REPLACEMENTS = {
    "CO": "COL",
    "COLOMBIA": "COL",
    "Colombia": "COL",
    "colombia": "COL",
}

CITY_REPLACEMENTS = {
    "bogotá": "Bogotá",
    "BOGOTÁ": "Bogotá",
    "Medellin": "Medellín",
    "medellín": "Medellín",
    "MEDELLÍN": "Medellín",
}


def clean_column_names(df):
    # Casos tipicos en la columna
    # ' Supplier ID ' -> "supplier_id"
    # 'City ' -> "city"
    # 'Purchase Date' -> "purchase_date"
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def clean_supplier_column(df):
    df["supplier"] = df["supplier"].str.strip()
    df["supplier"] = df["supplier"].replace(SUPPLIER_REPLACEMENTS)
    return df


def clean_country_column(df):
    df["country"] = df["country"].str.strip()
    df["country"] = df["country"].replace(COUNTRY_REPLACEMENTS)
    return df


def clean_city_column(df):
    df["city"] = df["city"].str.strip()
    df["city"] = df["city"].replace(CITY_REPLACEMENTS)
    return df


def clean_purchase_date_column(df):

    def convert_yyyy_s_mm_s_dd_to_yyyy_mm_dd(series):
        # Convierte fechas en formato "YYYY/MM/DD" a "YYYY-MM-DD"
        series = series.str.replace(r"(\d{4})/(\d{2})/(\d{2})", r"\1-\2-\3", regex=True)
        return series

    def convert_mmddyyyy_to_yyyy_mm_dd(series):
        # Corrige solo fechas con el día primero, cuando el día es mayor que 12.
        def convert_date(match):
            g1, g2, g3 = match.groups()
            if int(g2) > 12:  # el dia aparece en la mitad
                return f"{g3}-{g1}-{g2}"
            return f"{g3}-{g2}-{g1}"

        return series.str.replace(r"(\d{2})/(\d{2})/(\d{4})", convert_date, regex=True)

    def convert_dd_mm_yyyy_to_yyyy_mm_dd_separated_with_dots(series):
        # Corrige fechas en formato "DD.MM.YYYY" a "YYYY-MM-DD"
        return series.str.replace(r"(\d{2})\.(\d{2})\.(\d{4})", r"\3-\2-\1", regex=True)

    def convert_dd_mm_yy_to_yyyy_mm_dd_separated_with_hyphens(series):
        # Corrige fechas en formato "DD-MM-YY" a "YYYY-MM-DD"
        return series.str.replace(
            r"^(\d{2})-(\d{2})-(\d{2})$", r"20\3-\2-\1", regex=True
        )

    df["purchase_date"] = df["purchase_date"].str.strip()
    df["purchase_date"] = convert_yyyy_s_mm_s_dd_to_yyyy_mm_dd(df["purchase_date"])
    df["purchase_date"] = convert_mmddyyyy_to_yyyy_mm_dd(df["purchase_date"])
    df["purchase_date"] = convert_dd_mm_yyyy_to_yyyy_mm_dd_separated_with_dots(
        df["purchase_date"]
    )
    df["purchase_date"] = convert_dd_mm_yy_to_yyyy_mm_dd_separated_with_hyphens(
        df["purchase_date"]
    )

    return df


def clean_amount_column(df):

    def clean_strings_ending_with_k(series):
        # Convierte valores como "1.5K" a "1500"
        def convert_value(value):
            if isinstance(value, str) and value.endswith("K"):
                try:
                    return int(float(value[:-1]) * 1000)
                except ValueError:
                    return value
            return value

        return series.apply(convert_value)

    def clean_strings_starting_with_COP(series):
        # Convierte valores como "COP 1,250,000" a "1250000"
        def convert_value(value):
            if isinstance(value, str) and value.startswith("COP"):
                try:
                    return int(value[3:].replace(",", "").strip())
                except ValueError:
                    return value
            return value

        return series.apply(convert_value)

    def clean_strings_starting_with_dollar(series):
        # Convierte valores como "$1,250,000" a "1250000"
        def convert_value(value):
            if isinstance(value, str) and value.startswith("$"):
                try:
                    return int(value[1:].replace(",", "").strip())
                except ValueError:
                    return value
            return value

        return series.apply(convert_value)

    def remove_dots(series):
        # Elimina los puntos de los valores numéricos
        def convert_value(value):
            if isinstance(value, str):
                try:
                    return int(value.replace(".", "").strip())
                except ValueError:
                    return value
            return value

        return series.apply(convert_value)

    df["amount"] = df["amount"].str.strip()
    df["amount"] = clean_strings_ending_with_k(df["amount"])
    df["amount"] = clean_strings_starting_with_COP(df["amount"])
    df["amount"] = clean_strings_starting_with_dollar(df["amount"])
    df["amount"] = remove_dots(df["amount"])

    return df


def clean_discount_column(df):
    # Limpia la columna de descuento
    df["discount"] = df["discount"].str.strip()
    df["discount"] = df["discount"].str.replace("%", "", regex=False)
    df["discount"] = df["discount"].map(
        lambda x: float(x) / 100 if not pd.isna(x) and float(x) > 1 else x
    )

    return df
def clean_supplier_id_column(df):
    # ' 0007 ' -> '0007'
    df["supplier_id"] = df["supplier_id"].astype(str).str.strip().str.zfill(4)
    return df


def clean_weight_column(df):
    # Normaliza todo a kg: "50000 g", "0.0050 ton", "2,5 kg", "12" -> float en kg
    factors = {"g": 0.001, "kg": 1, "ton": 1000}

    def convert_value(value):
        if pd.isna(value):
            return value
        v = str(value).strip().lower().replace(",", ".")
        match = re.fullmatch(r"([\d.]+)\s*(kg|g|ton)?", v)
        if not match:
            return pd.NA
        number = float(match.group(1))
        unit = match.group(2) or "kg"  # sin unidad se asume kg
        return round(number * factors[unit], 3)

    df["weight"] = df["weight"].apply(convert_value)
    return df


def clean_units_column(df):
    # "N/A" -> NaN, resto a entero
    df["units"] = pd.to_numeric(df["units"], errors="coerce").astype("Int64")
    return df


def clean_unit_price_column(df):
    # "$125,000.00", "980.000.00", "$-1,750,000.00" -> float
    def convert_value(value):
        if pd.isna(value):
            return value
        v = str(value).strip().replace("$", "").replace(",", "")
        if v.count(".") > 1:  # puntos como separador de miles
            integer_part, decimal_part = v.rsplit(".", 1)
            v = integer_part.replace(".", "") + "." + decimal_part
        try:
            return abs(float(v))  # un precio no puede ser negativo
        except ValueError:
            return pd.NA

    df["unit_price"] = df["unit_price"].apply(convert_value)
    return df


def clean_contact_email_column(df):
    # "sin correo" -> NaN
    df["contact_email"] = df["contact_email"].str.strip().str.lower()
    df["contact_email"] = df["contact_email"].replace("sin correo", pd.NA)
    return df


def remove_duplicates(df):
    # Elimina las filas repetidas (0005, 0010, 0019)
    return df.drop_duplicates(subset="supplier_id", keep="first")

def main():
    df = pd.read_csv(INPUT_FILE)
    df = clean_column_names(df)
    df = clean_supplier_id_column(df)
    df = clean_supplier_column(df)
    df = clean_country_column(df)
    df = clean_city_column(df)
    df = clean_purchase_date_column(df)
    df = clean_amount_column(df)
    df = clean_discount_column(df)
    df = clean_weight_column(df)
    df = clean_units_column(df)
    df = clean_unit_price_column(df)
    df = clean_contact_email_column(df)
    df = remove_duplicates(df)
    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()