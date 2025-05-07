import streamlit as st
import pandas as pd
from mainapp import fetch_flight_data, prepare_dataframe
from database import save_to_database, load_from_database, query_average_price_per_weekday

st.set_page_config(page_title="Flugpreis Analyse", layout="wide")
st.title("✈️ Flugpreis-Analyse")

origin = st.text_input("Abflughafen", "ZRH")
destination = st.text_input("Zielflughafen", "BCN")

col1, col2 = st.columns(2)

# Button 1: Daten von API holen und speichern
with col1:
    if st.button("🔄 Daten von API abrufen"):
        raw_data = fetch_flight_data(origin, destination, currency="CHF")
        df = prepare_dataframe(raw_data)

        if df.empty:
            st.warning("❌ Keine Daten von der API empfangen.")
        else:
            save_to_database(df)
            st.success(f"✅ {len(df)} Flüge gespeichert.")
            st.dataframe(df)

# Button 2: Daten aus Datenbank laden
with col2:
    if st.button("📂 Daten aus Datenbank laden"):
        df = load_from_database()

        if df.empty:
            st.warning("📭 Keine Daten in der Datenbank gefunden.")
        else:
            st.success(f"📊 {len(df)} Flüge geladen.")
            st.dataframe(df)

            st.subheader("📈 Preisverlauf")
            st.line_chart(df.set_index("Reisedatum")["Preis (CHF)"])

            st.subheader("📊 Durchschnittspreis nach Wochentag")
            df["weekday"] = pd.to_datetime(df["Reisedatum"]).dt.day_name()
            st.bar_chart(df.groupby("weekday")["Preis (CHF)"].mean())

            st.subheader("🧠 SQL-Auswertung aus DB")
            sql_df = query_average_price_per_weekday()
            st.dataframe(sql_df)
            
#Zum Ordner /workspaces/group01_flights/flugpreis-analyse-sp2025 navigieren und ausführen: run app/app_streamlit.py