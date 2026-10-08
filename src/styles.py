"""Custom CSS für ein professionelles Erscheinungsbild."""
import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
        /* --- Farbpalette --- */
        :root {
            --brand-primary: #0f766e;
            --brand-primary-light: #14b8a6;
            --brand-accent: #f59e0b;
            --brand-dark: #0f172a;
            --brand-muted: #64748b;
            --brand-bg: #f8fafc;
            --brand-card: #ffffff;
            --brand-border: #e2e8f0;
        }

        /* --- Grundlayout --- */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* --- Hero Header --- */
        .hero {
            background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
            padding: 2.5rem 2rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(15, 118, 110, 0.3);
        }
        .hero h1 {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0 0 0.5rem 0;
            letter-spacing: -0.02em;
            color: white !important;
        }
        .hero p {
            font-size: 1.1rem;
            opacity: 0.95;
            margin: 0;
            font-weight: 400;
        }
        .hero .author {
            margin-top: 1rem;
            font-size: 0.9rem;
            opacity: 0.85;
            font-weight: 500;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        /* --- Section Headers --- */
        h2 {
            color: var(--brand-dark) !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em;
            margin-top: 1.5rem !important;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--brand-border);
        }
        h3 {
            color: var(--brand-dark) !important;
            font-weight: 600 !important;
        }

        /* --- Metric Cards --- */
        div[data-testid="stMetric"] {
            background: var(--brand-card);
            padding: 1.25rem 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--brand-border);
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: all 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            box-shadow: 0 4px 12px rgba(15, 118, 110, 0.1);
            border-color: var(--brand-primary-light);
        }
        div[data-testid="stMetricLabel"] {
            color: var(--brand-muted) !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="stMetricValue"] {
            color: var(--brand-dark) !important;
            font-weight: 700 !important;
        }

        /* --- Buttons --- */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
            color: white;
            border: none;
            padding: 0.6rem 2rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            letter-spacing: 0.02em;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(15, 118, 110, 0.2);
        }
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(15, 118, 110, 0.35);
        }

        /* --- Sidebar --- */
        section[data-testid="stSidebar"] {
            background: #0f172a;
        }
        section[data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }
        section[data-testid="stSidebar"] h1 {
            color: white !important;
            font-size: 1.5rem !important;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 1.5rem;
        }
        section[data-testid="stSidebar"] .stRadio > label {
            color: #94a3b8 !important;
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
        }
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
            background: transparent;
            border-radius: 8px;
            padding: 0.5rem 0.75rem;
            margin: 0.15rem 0;
            transition: background 0.15s;
            cursor: pointer;
        }
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
            background: rgba(20, 184, 166, 0.15);
        }

        /* --- Dataframe styling --- */
        div[data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid var(--brand-border);
        }

        /* --- Success / Warning / Info boxes --- */
        div[data-testid="stAlert"] {
            border-radius: 10px;
            border-left: 4px solid;
        }

        /* --- Footer --- */
        .app-footer {
            margin-top: 3rem;
            padding: 1.5rem 0;
            border-top: 1px solid var(--brand-border);
            color: var(--brand-muted);
            font-size: 0.85rem;
            text-align: center;
        }
        .app-footer a {
            color: var(--brand-primary);
            text-decoration: none;
            font-weight: 500;
            margin: 0 0.5rem;
        }
        .app-footer a:hover {
            text-decoration: underline;
        }

        /* --- Hide default Streamlit chrome --- */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {
            background: transparent;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, tagline: str, author: str, version: str):
    """Rendert das Hero-Header-Element."""
    st.markdown(
        f"""
        <div class="hero">
            <h1>🏠 {title}</h1>
            <p>{tagline}</p>
            <div class="author">von {author} · Version {version}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer(author: str, github: str, linkedin: str, version: str):
    """Rendert den Footer mit Links."""
    st.markdown(
        f"""
        <div class="app-footer">
            <strong>Mietcheck</strong> · Version {version} · © 2026 {author}<br>
            <a href="{github}" target="_blank">GitHub</a> ·
            <a href="{linkedin}" target="_blank">LinkedIn</a>
            <br><br>
            Datenquelle: Kuratierte Mietspiegel-Daten 2019–2024 · Alle Angaben ohne Gewähr.
        </div>
        """,
        unsafe_allow_html=True,
    )
