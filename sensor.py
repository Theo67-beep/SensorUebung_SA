"""
SensorPy – Messdaten analysieren
=================================
Dieses Modul enthält alle Funktionen zur Analyse von Umweltmessdaten.

Aufgabe: Implementiert jede Funktion so, dass sie der Beschreibung
im Docstring entspricht. Die Signatur (Name, Parameter, Rückgabetyp)
darf NICHT verändert werden.

Datenformat (eine Zeile aus messdaten.csv als dict):
    {
        "sensor_id":       "S01",
        "timestamp":       "2024-03-01 08:00",
        "temperatur":      19.2,
        "luftfeuchtigkeit": 52.1,
        "co2":             480.0
    }
"""

import csv


# ──────────────────────────────────────────────────────────────
# PERSON A
# ──────────────────────────────────────────────────────────────

def load_data(filename: str) -> list[dict]:
    """Liest CSV ein, konvertiert numerische Felder zu float. Leere Liste bei Fehler."""
    numeric_fields = {"temperatur", "luftfeuchtigkeit", "co2"}
    result = []
    try:
        with open(filename, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                entry = {k.strip(): float(v) if k.strip() in numeric_fields else v.strip()
                         for k, v in row.items()}
                result.append(entry)
    except (FileNotFoundError, OSError, ValueError):
        return []
    return result



def calculate_average(values: list[float]) -> float:
    """Durchschnitt, gerundet auf 2 Dezimalstellen."""
    return round(sum(values) / len(values), 2)


def find_extremes(values: list[float]) -> tuple[float, float]:
    """Gibt (min, max) zurück."""
    return (min(values), max(values))

def count_above_threshold(values: list[float], threshold: float) -> int:
    """Anzahl der Werte strikt grösser als threshold."""
    return sum(1 for v in values if v > threshold)


# ──────────────────────────────────────────────────────────────
# PERSON B
# ──────────────────────────────────────────────────────────────

def classify_value(value: float, limits: dict) -> str:
    if value < limits["niedrig"]:
        return "niedrig"
    elif value < limits["normal"]:
        return "normal"
    elif value < limits["hoch"]:
        return "hoch"
    else:
        return "kritisch"


def filter_by_sensor(data: list[dict], sensor_id: str) -> list[dict]:
    return [entry for entry in data if entry["sensor_id"] == sensor_id]


def generate_report(data: list[dict]) -> str:
    if not data:
        return "========== SensorPy Bericht ==========\nKeine Daten vorhanden.\n======================================"

    total      = len(data)
    sensor_ids = sorted({entry["sensor_id"] for entry in data})

    temperatures = [entry["temperatur"]       for entry in data]
    humidities   = [entry["luftfeuchtigkeit"] for entry in data]
    co2_values   = [entry["co2"]              for entry in data]

    critical_temp_count = sum(1 for t in temperatures if t > 30)

    def avg(values: list[float]) -> float:
        return sum(values) / len(values)

    lines = [
        "========== SensorPy Bericht ==========",
        f"Messungen total:       {total}",
        f"Sensoren:              {', '.join(sensor_ids)}",
        "",
        "-- Temperatur (°C) --",
        f"Durchschnitt:          {avg(temperatures):.2f}",
        f"Min / Max:             {min(temperatures)} / {max(temperatures)}",
        f"Kritische Werte (>30): {critical_temp_count}",
        "",
        "-- Luftfeuchtigkeit (%) --",
        f"Durchschnitt:          {avg(humidities):.2f}",
        f"Min / Max:             {min(humidities)} / {max(humidities)}",
        "",
        "-- CO2 (ppm) --",
        f"Durchschnitt:          {avg(co2_values):.2f}",
        f"Min / Max:             {min(co2_values)} / {max(co2_values)}",
        "======================================",
    ]

    return "\n".join(lines)
