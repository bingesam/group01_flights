# Flight Price Analysis (Scientific Programming FS2025)

This project investigates how flight prices vary depending on the day of the week, destination, and season. The data is retrieved via the Travelpayouts API, stored in a SQLite database, and analyzed in an interactive Streamlit app.
---

## Team

- Delia Troncato
- Samira Binggesser
- Gioia Finocchi

---

## Contents

- Web API integration (Travelpayouts)
- Data preparation with Pandas including type conversion
- Use of regular expressions (regex) to extract time information
- Use of Python data structures (lists, dictionaries, etc.)
- Control structures: conditions and loops
- Exploratory data analysis and visualizations (Matplotlib, Seaborn)
- Statistical analysis (t-test with p-value)
- Storage in a SQLite database including SQL query
- Interactive Streamlit web app for presentation and analysis
- Analysis with a Large Language Model (LLM) via Together.ai
- Analysis in a Jupyter Notebook

---

## Projekt starten

### 1. Clone the repository (if not already done)
### 2. Create a .env file with your API credentials
Contents of the .env file:

TRAVELPAYOUTS_TOKEN=your_token_here 
TOGETHER_API_KEY=your_token_here 

> Important: **Do not upload this file to the repository** – it contains private credentials! 

### 3. Install required packages

pip install -r requirements.txt

### 4. Start the Streamlit web app

streamlit run app/app_streamlit.py

-> The app will run locally in the browser at http://localhost:8501

---

## Jupyter notebook

The accompanying Jupyter notebook can be used for further analysis and visualization:

### Start notebook

jupyter lab notebooks/flugpreis_analyse.ipynb

Alternatively, open directly in VS Code under the notebooks/ folder.


