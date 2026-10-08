"""Kernlogik für Mietpreis-Analysen."""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def check_fair_rent(
    df: pd.DataFrame, city: str, district: str, size: float, rent: float
) -> dict:
    """Vergleicht die angegebene Miete mit dem lokalen Durchschnitt."""
    subset = df[(df["stadt"] == city) & (df["stadtteil"] == district)]
    if subset.empty:
        subset = df[df["stadt"] == city]

    avg_per_sqm = subset["miete_pro_m2"].mean()
    fair_rent = avg_per_sqm * size
    difference = rent - fair_rent
    difference_percent = (difference / fair_rent) * 100

    if difference_percent < -10:
        status = "low"
    elif difference_percent <= 10:
        status = "fair"
    else:
        status = "high"

    return {
        "avg_rent": fair_rent,
        "avg_per_sqm": avg_per_sqm,
        "difference": difference,
        "difference_percent": difference_percent,
        "status": status,
    }


def get_city_average(df: pd.DataFrame, city: str) -> float:
    """Durchschnittliche Miete pro m² für eine Stadt."""
    return df[df["stadt"] == city]["miete_pro_m2"].mean()


def get_district_averages(df: pd.DataFrame, city: str) -> pd.DataFrame:
    """Durchschnitt pro Stadtteil für eine Stadt."""
    return (
        df[df["stadt"] == city]
        .groupby("stadtteil")["miete_pro_m2"]
        .mean()
        .reset_index()
        .sort_values("miete_pro_m2", ascending=False)
    )


def get_city_trend(historical_df: pd.DataFrame, city: str) -> pd.DataFrame:
    """
    Berechnet den durchschnittlichen Mietverlauf pro Jahr für eine Stadt.
    """
    city_df = historical_df[historical_df["stadt"] == city]
    trend = (
        city_df.groupby("jahr")["miete_pro_m2"]
        .mean()
        .reset_index()
        .sort_values("jahr")
    )
    return trend


def get_city_cagr(historical_df: pd.DataFrame, city: str) -> float:
    """Berechnet die jährliche Wachstumsrate (CAGR) der Mieten für eine Stadt."""
    trend = get_city_trend(historical_df, city)
    if len(trend) < 2:
        return 0.0
    first = trend.iloc[0]["miete_pro_m2"]
    last = trend.iloc[-1]["miete_pro_m2"]
    years = trend.iloc[-1]["jahr"] - trend.iloc[0]["jahr"]
    if years == 0 or first == 0:
        return 0.0
    return ((last / first) ** (1 / years) - 1) * 100


def predict_fair_rent(
    df: pd.DataFrame, city: str, district: str, size: float
) -> dict:
    """
    Prognostiziert die faire Miete mittels linearer Regression
    auf Basis von Wohnfläche und Stadtteil-Durchschnitt.
    """
    city_df = df[df["stadt"] == city].copy()

    # Feature 1: Wohnfläche (simuliert via Stadtteil-Mittelwert als Proxy)
    # Feature 2: Stadtteil-Durchschnittspreis
    city_df["district_avg"] = city_df["stadtteil"].map(
        city_df.groupby("stadtteil")["miete_pro_m2"].mean()
    )

    # Trainingsdaten: generiere synthetische Samples aus Stadtteil-Durchschnitt
    X = []
    y = []
    for _, row in city_df.iterrows():
        for size_sample in [40, 60, 80, 100, 120]:
            X.append([size_sample, row["district_avg"]])
            y.append(size_sample * row["miete_pro_m2"])

    X = np.array(X)
    y = np.array(y)

    model = LinearRegression()
    model.fit(X, y)

    district_avg = city_df[city_df["stadtteil"] == district]["district_avg"].mean()
    if pd.isna(district_avg):
        district_avg = city_df["district_avg"].mean()

    predicted = model.predict([[size, district_avg]])[0]
    r2 = model.score(X, y)

    return {
        "predicted_rent": max(predicted, 0),
        "model_r2": r2,
        "district_avg_per_sqm": district_avg,
    }
