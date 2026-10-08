"""Modul zum Laden und Vorbereiten der Mietdaten."""
from pathlib import Path
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent.parent / "data"


@st.cache_data
def load_rent_data(filename: str = "mietspiegel_2024.csv") -> pd.DataFrame:
    """Lädt die aktuellen Mietspiegel-Daten (ein Jahr)."""
    df = pd.read_csv(DATA_DIR / filename)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


@st.cache_data
def load_historical_data(filename: str = "mietspiegel_historical.csv") -> pd.DataFrame:
    """Lädt die historischen Mietdaten (mehrere Jahre)."""
    df = pd.read_csv(DATA_DIR / filename)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


@st.cache_data
def load_coordinates(filename: str = "staedte_koordinaten.csv") -> pd.DataFrame:
    """Lädt die Koordinaten der Stadtteile."""
    df = pd.read_csv(DATA_DIR / filename)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def get_city_list(df: pd.DataFrame) -> list[str]:
    """Gibt eine sortierte Liste der Städte zurück."""
    return sorted(df["stadt"].unique())


def get_district_list(df: pd.DataFrame, city: str) -> list[str]:
    """Gibt eine sortierte Liste der Stadtteile für eine Stadt zurück."""
    return sorted(df[df["stadt"] == city]["stadtteil"].unique())
