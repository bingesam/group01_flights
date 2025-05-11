# Import necessary libraries
import sqlite3
import pandas as pd

# Function to save a DataFrame to a SQLite database
def save_to_database(df, db_path="/workspaces/group01_flights/flugpreis-analyse-sp2025/data/fluege.db"):
    conn = sqlite3.connect(db_path)  # Establish connection to the database
    df.to_sql("flugpreise", conn, if_exists="replace", index=False)  # Save the DataFrame to table 'flugpreise' (replace if exists)
    conn.close()  # Close the connection

# Function to load all flight data from the database
def load_from_database(db_path="/workspaces/group01_flights/flugpreis-analyse-sp2025/data/fluege.db"):
    conn = sqlite3.connect(db_path)  # Open connection
    try:
        df = pd.read_sql("SELECT * FROM flugpreise", conn)  # SQL query to load all data
    except Exception as e:
        print("Error loading from database:", e)  # Handle errors (e.g., table does not exist)
        df = pd.DataFrame()  # Return empty DataFrame to avoid crash
    conn.close()
    return df  # Return result

# Function to query average flight price per weekday (using raw SQL)
def query_average_price_per_weekday(db_path="/workspaces/group01_flights/flugpreis-analyse-sp2025/data/fluege.db"):
    conn = sqlite3.connect(db_path)  # Open database connection
    query = """
    SELECT strftime('%w', Reisedatum) AS WochentagNum,  -- Extract numeric weekday (0=Sunday, ..., 6=Saturday)
           CASE strftime('%w', Reisedatum)              -- Convert weekday number to weekday name
               WHEN '0' THEN 'Sunday'
               WHEN '1' THEN 'Monday'
               WHEN '2' THEN 'Tuesday'
               WHEN '3' THEN 'Wednesday'
               WHEN '4' THEN 'Thursday'
               WHEN '5' THEN 'Friday'
               WHEN '6' THEN 'Saturday'
           END AS Wochentag,
           AVG("Preis (CHF)") AS Durchschnittspreis     -- Calculate average price per day
    FROM flugpreise
    GROUP BY WochentagNum                                -- Group by numeric weekday (to maintain correct order)
    ORDER BY WochentagNum                                -- Sort by weekday number (not alphabetically)
    """
    df = pd.read_sql(query, conn)  # Execute SQL query and load result into DataFrame
    conn.close()  # Close connection
    return df     # Return result
