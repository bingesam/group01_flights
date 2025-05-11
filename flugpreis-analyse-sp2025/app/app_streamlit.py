# Import required libraries
import streamlit as st                 # For the web app interface
import pandas as pd                   # For data manipulation
from mainapp import fetch_flight_data, prepare_dataframe  # Functions for API data fetching and processing
from database import save_to_database, load_from_database, query_average_price_per_weekday  # DB utilities
from mainapp import together_explain_weekday_prices        # AI analysis using Together.ai

# Streamlit base settings
st.set_page_config(page_title="Flight Price Analysis", layout="wide")
st.title("Flight Price Analysis")

# Initialize session state for DataFrame (only on first load)
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

# User input: origin and destination airport codes
origin = st.text_input("Departure Airport", "ZRH")
destination = st.text_input("Arrival Airport", "BCN")

# Two columns side-by-side for buttons
col1, col2 = st.columns(2)

# Fetch data live via API
with col1:
    if st.button("Fetch data from API"):
        raw_data = fetch_flight_data(origin, destination, currency="CHF")  # API request
        df = prepare_dataframe(raw_data)  # Format data into a DataFrame

        if df.empty:
            st.warning("No data received from API.")
        else:
            st.session_state.df = df        # Save to session state
            save_to_database(df)            # Optionally save to SQLite
            st.success(f"{len(df)} flights saved.")
            st.dataframe(df)                # Display as table in app

# Load data locally from SQLite database
with col2:
    if st.button("Load data from database"):
        df = load_from_database()

        if df.empty:
            st.warning("No data found in the database.")
        else:
            st.session_state.df = df
            st.success(f"{len(df)} flights loaded.")
            st.dataframe(df)

# Display visualizations only if data is available
if not st.session_state.df.empty:
    df = st.session_state.df

    # Line chart: price trend over time
    st.subheader("Price Trend")
    st.line_chart(df.set_index("Reisedatum")["Preis (CHF)"])

    # Bar chart: average price per weekday
    st.subheader("Average Price by Weekday")
    df["weekday"] = pd.to_datetime(df["Reisedatum"]).dt.day_name()
    st.bar_chart(df.groupby("weekday")["Preis (CHF)"].mean())

    # SQL-based analysis: weekday grouping from DB
    st.subheader("SQL-Based Analysis (from Database)")
    sql_df = query_average_price_per_weekday()
    st.dataframe(sql_df)
else:
    st.info("ℹ️ Please fetch or load flight data first.")

# AI analysis with Together.ai
if not st.session_state.df.empty:
    st.subheader("AI Analysis (Together.ai)")

    df = st.session_state.df
    if "weekday" not in df.columns:
        df["weekday"] = pd.to_datetime(df["Reisedatum"]).dt.day_name()

    if st.button("Start Together AI Analysis"):
        try:
            result = together_explain_weekday_prices(df)
            st.success("AI Response received:")
            st.write(result)
        except Exception as e:
            st.error("Error when querying Together.ai")
            st.exception(e)

# Run app from terminal:
# Navigate to /workspaces/group01_flights/flugpreis-analyse-sp2025/app and run:
# ➜ streamlit run app_streamlit.py