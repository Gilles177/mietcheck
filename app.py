"""Mietcheck – Mietpreisanalyse für Deutschland."""
import streamlit as st
import plotly.express as px
import pandas as pd

from src.config import (
    AUTHOR_NAME,
    GITHUB_URL,
    LINKEDIN_URL,
    APP_VERSION,
    APP_TAGLINE,
)
from src.styles import inject_custom_css, render_hero, render_footer
from src.data_loader import (
    load_rent_data,
    load_historical_data,
    load_coordinates,
    get_city_list,
    get_district_list,
)
from src.analysis import (
    check_fair_rent,
    get_district_averages,
    get_city_trend,
    get_city_cagr,
    predict_fair_rent,
)

# --- Seitenkonfiguration ---
st.set_page_config(
    page_title="Mietcheck – Mietpreisanalyse Deutschland",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling ---
inject_custom_css()

# --- Daten laden ---
df = load_rent_data()
hist_df = load_historical_data()
coords_df = load_coordinates()
staedte = get_city_list(df)

# --- Sidebar ---
st.sidebar.title("🏠 Mietcheck")
st.sidebar.markdown(
    f"<p style='color:#94a3b8;font-size:0.85rem;margin-top:-0.5rem;'>"
    f"{APP_TAGLINE}</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

seite = st.sidebar.radio(
    "Navigation",
    [
        "Mietpreis-Checker",
        "Markttrends",
        "Städtevergleich",
        "Karte",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style='font-size:0.75rem;color:#94a3b8;'>
        <strong style='color:#e2e8f0;'>{AUTHOR_NAME}</strong><br>
        Version {APP_VERSION}<br><br>
        <a href="{GITHUB_URL}" target="_blank" style="color:#14b8a6;text-decoration:none;">GitHub</a> ·
        <a href="{LINKEDIN_URL}" target="_blank" style="color:#14b8a6;text-decoration:none;">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Hero Header (auf jeder Seite) ---
PAGE_TITLES = {
    "Mietpreis-Checker": ("Ist meine Miete fair?", "Vergleichen Sie Ihre Miete mit aktuellen Marktdaten."),
    "Markttrends": ("Markttrends für Mieten", "Die Entwicklung der Mietpreise in deutschen Großstädten 2019–2024."),
    "Städtevergleich": ("Städtevergleich", "Mietniveaus in deutschen Großstädten im direkten Vergleich."),
    "Karte": ("Mietkarte Deutschland", "Geografische Verteilung der Mietpreise in Stadtteilen."),
}
hero_title, hero_sub = PAGE_TITLES[seite]
render_hero(hero_title, hero_sub, AUTHOR_NAME, APP_VERSION)


# =============================================================
# Seite 1: Mietpreis-Checker
# =============================================================
if seite == "Mietpreis-Checker":
    st.markdown("### Ihre Angaben")

    col1, col2, col3 = st.columns(3)
    with col1:
        stadt = st.selectbox("Stadt", staedte)
    with col2:
        stadtteile = get_district_list(df, stadt)
        stadtteil = st.selectbox("Stadtteil", stadtteile)
    with col3:
        groesse = st.number_input(
            "Wohnfläche (m²)", min_value=10, max_value=500, value=70, step=1
        )

    kaltmiete = st.number_input(
        "Ihre Kaltmiete (€/Monat)",
        min_value=100,
        max_value=10000,
        value=1200,
        step=50,
    )

    st.markdown("")

    if st.button("Miete prüfen", type="primary"):
        result = check_fair_rent(df, stadt, stadtteil, groesse, kaltmiete)
        prediction = predict_fair_rent(df, stadt, stadtteil, groesse)

        st.markdown("### Ergebnis")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Ø vor Ort", f"{result['avg_per_sqm']:.2f} €/m²")
        m2.metric("Faire Miete", f"{result['avg_rent']:.0f} €")
        m3.metric(
            "Modell-Prognose",
            f"{prediction['predicted_rent']:.0f} €",
            f"R² = {prediction['model_r2']:.2f}",
            delta_color="off",
        )
        m4.metric(
            "Abweichung",
            f"{result['difference']:+.0f} €",
            f"{result['difference_percent']:+.1f} %",
            delta_color="inverse",
        )

        if result["status"] == "fair":
            st.success(
                f"**Ihre Miete ist fair.** Sie liegt im Rahmen des ortsüblichen "
                f"Durchschnitts für {stadtteil}, {stadt}."
            )
        elif result["status"] == "high":
            st.warning(
                f"**Ihre Miete liegt über dem Durchschnitt.** Sie zahlen etwa "
                f"{result['difference_percent']:.1f} % mehr als der lokale Durchschnitt."
            )
        else:
            st.info(
                f"**Ihre Miete ist günstig.** Sie zahlen etwa "
                f"{abs(result['difference_percent']):.1f} % weniger als der lokale Durchschnitt."
            )

        st.markdown("---")
        st.markdown(f"### Mietniveau in {stadt}")
        dist_df = get_district_averages(df, stadt)

        fig = px.bar(
            dist_df,
            x="miete_pro_m2",
            y="stadtteil",
            orientation="h",
            labels={"miete_pro_m2": "Miete (€/m²)", "stadtteil": ""},
            color="miete_pro_m2",
            color_continuous_scale=["#ccfbf1", "#0f766e"],
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================================================
# Seite 2: Markttrends
# =============================================================
elif seite == "Markttrends":
    auswahl_staedte = st.multiselect(
        "Städte auswählen", staedte, default=staedte, key="trend_cities",
    )

    if not auswahl_staedte:
        st.info("Bitte mindestens eine Stadt auswählen.")
    else:
        rows = []
        for stadt_name in auswahl_staedte:
            trend = get_city_trend(hist_df, stadt_name)
            trend["stadt"] = stadt_name
            rows.append(trend)

        trend_all = pd.concat(rows, ignore_index=True)

        fig = px.line(
            trend_all,
            x="jahr",
            y="miete_pro_m2",
            color="stadt",
            markers=True,
            labels={"jahr": "Jahr", "miete_pro_m2": "Miete (€/m²)", "stadt": "Stadt"},
            color_discrete_sequence=["#0f766e", "#14b8a6", "#f59e0b", "#8b5cf6", "#ef4444"],
        )
        fig.update_layout(
            height=450,
            margin=dict(l=0, r=0, t=20, b=0),
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Jährliche Wachstumsrate (CAGR)")
        cagr_data = []
        for stadt_name in auswahl_staedte:
            cagr = get_city_cagr(hist_df, stadt_name)
            trend = get_city_trend(hist_df, stadt_name)
            start = trend.iloc[0]["miete_pro_m2"]
            end = trend.iloc[-1]["miete_pro_m2"]
            cagr_data.append(
                {
                    "Stadt": stadt_name,
                    "2019 (€/m²)": f"{start:.2f}",
                    "2024 (€/m²)": f"{end:.2f}",
                    "CAGR (%)": f"{cagr:+.2f}",
                }
            )
        st.dataframe(cagr_data, use_container_width=True, hide_index=True)

# =============================================================
# Seite 3: Städtevergleich
# =============================================================
elif seite == "Städtevergleich":
    auswahl = st.multiselect(
        "Städte auswählen", staedte, default=staedte[:3], key="compare_cities",
    )

    if not auswahl:
        st.info("Bitte mindestens eine Stadt auswählen.")
    else:
        avg_df = (
            df[df["stadt"].isin(auswahl)]
            .groupby("stadt")["miete_pro_m2"]
            .mean()
            .reset_index()
            .sort_values("miete_pro_m2", ascending=False)
        )

        fig = px.bar(
            avg_df,
            x="stadt",
            y="miete_pro_m2",
            labels={"stadt": "", "miete_pro_m2": "Miete (€/m²)"},
            color="stadt",
            text_auto=".2f",
            color_discrete_sequence=["#0f766e", "#14b8a6", "#f59e0b", "#8b5cf6", "#ef4444"],
        )
        fig.update_layout(
            height=450,
            showlegend=False,
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Detailansicht nach Stadtteil")
        pivot = (
            df[df["stadt"].isin(auswahl)]
            .pivot_table(
                index="stadtteil",
                columns="stadt",
                values="miete_pro_m2",
                aggfunc="mean",
            )
            .round(2)
        )
        st.dataframe(pivot, use_container_width=True)

# =============================================================
# Seite 4: Karte
# =============================================================
elif seite == "Karte":
    auswahl = st.multiselect(
        "Städte auswählen", staedte, default=staedte, key="map_cities",
    )

    if not auswahl:
        st.info("Bitte mindestens eine Stadt auswählen.")
    else:
        merged = df.merge(coords_df, on=["stadt", "stadtteil"], how="inner")
        merged = merged[merged["stadt"].isin(auswahl)]

        if merged.empty:
            st.warning("Keine übereinstimmenden Koordinaten gefunden.")
        else:
            fig = px.scatter_map(
                merged,
                lat="lat",
                lon="lon",
                color="miete_pro_m2",
                size="miete_pro_m2",
                hover_name="stadtteil",
                hover_data={
                    "stadt": True,
                    "miete_pro_m2": ":.2f",
                    "lat": False,
                    "lon": False,
                },
                color_continuous_scale=["#0f766e", "#f59e0b", "#dc2626"],
                size_max=30,
                zoom=5,
                center={"lat": 51.0, "lon": 10.5},
                map_style="open-street-map",
                labels={"miete_pro_m2": "Miete (€/m²)"},
            )
            fig.update_layout(height=650, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Top 10 teuerste Stadtteile")
            top10 = merged.nlargest(10, "miete_pro_m2")[
                ["stadt", "stadtteil", "miete_pro_m2"]
            ].reset_index(drop=True)
            top10.index += 1
            st.dataframe(top10, use_container_width=True)

# --- Footer ---
render_footer(AUTHOR_NAME, GITHUB_URL, LINKEDIN_URL, APP_VERSION)
