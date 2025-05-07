import streamlit as st
import pandas as pd
from mainapp import fetch_flight_data, prepare_dataframe
from database import save_to_database, load_from_database, query_average_price_per_weekday
from mainapp import together_explain_weekday_prices


st.set_page_config(page_title="Flugpreis Analyse", layout="wide")
st.title("✈️ Flugpreis-Analyse")

# Session-State für df vorbereiten
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

origin = st.text_input("Abflughafen", "ZRH")
destination = st.text_input("Zielflughafen", "BCN")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Daten von API abrufen"):
        raw_data = fetch_flight_data(origin, destination, currency="CHF")
        df = prepare_dataframe(raw_data)

        if df.empty:
            st.warning("❌ Keine Daten von der API empfangen.")
        else:
            st.session_state.df = df
            save_to_database(df)
            st.success(f"✅ {len(df)} Flüge gespeichert.")
            st.dataframe(df)

with col2:
    if st.button("📂 Daten aus Datenbank laden"):
        df = load_from_database()

        if df.empty:
            st.warning("📭 Keine Daten in der Datenbank gefunden.")
        else:
            st.session_state.df = df
            st.success(f"📊 {len(df)} Flüge geladen.")
            st.dataframe(df)

# Visualisierung nur wenn Daten da
if not st.session_state.df.empty:
    df = st.session_state.df

    st.subheader("📈 Preisverlauf")
    st.line_chart(df.set_index("Reisedatum")["Preis (CHF)"])

    st.subheader("📊 Durchschnittspreis pro Wochentag")
    df["weekday"] = pd.to_datetime(df["Reisedatum"]).dt.day_name()
    st.bar_chart(df.groupby("weekday")["Preis (CHF)"].mean())

    st.subheader("📋 SQL-Auswertung (aus Datenbank)")
    sql_df = query_average_price_per_weekday()
    st.dataframe(sql_df)
else:
    st.info("ℹ️ Bitte zuerst Daten abrufen oder laden.")

#Together AI
if not st.session_state.df.empty:
    st.subheader("💬 KI-Auswertung (Together.ai)")

    df = st.session_state.df
    if "weekday" not in df.columns:
        df["weekday"] = pd.to_datetime(df["Reisedatum"]).dt.day_name()

    if st.button("🧠 Together AI Analyse starten"):
        try:
            result = together_explain_weekday_prices(df)
            st.success("✅ Antwort erhalten:")
            st.write(result)
        except Exception as e:
            st.error("❌ Fehler bei der Anfrage an Together.ai")
            st.exception(e)



#Zum Ordner /workspaces/group01_flights/flugpreis-analyse-sp2025/app navigieren und ausführen: streamlit run app_streamlit.py
