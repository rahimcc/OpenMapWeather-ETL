import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import datetime



st_autorefresh(interval = 60 * 1000, key = "datarefresh")
st.caption(f'Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')

conn = st.connection("postgresql", type="sql")

@st.cache_data(ttl=60)
def load_current():
    query = """
            SELECT
                recorded_at,
                temp,
                humidity,
                weather_condition
            FROM raw.weather_readings
            ORDER BY recorded_at DESC
            LIMIT 200 
        """
    return conn.query(query)


@st.cache_data(ttl = 60 )
def load_summary():
    query = """
            SELECT * 
            FROM dbt_dev.daily_weather_summary 
            ORDER BY day DESC
            LIMIT 10
            """
    return conn.query(query)


st.set_page_config(page_title = "Baku Weather Dashboard", layout="wide")
st.title("🌤️ Baku Weather Dashboard")
st.write("Hello — Streamlit is running.")


df_current = load_current()
df_summary = load_summary()



#st.dataframe(df_summary)

df_current['temp'] = round(df_current['temp'] - 273.15,2)
df_summary['avg_temp'] = round(df_summary['avg_temp'] - 273.15,2) 
df_summary['date'] = pd.to_datetime(df_summary['day']).dt.strftime('%Y-%m-%d')

latest = df_current.iloc[0]
col1,col2,col3= st.columns(3)

col1.metric("Current temperature", f'{latest['temp']}°C')
col2.metric("Humidity", f'{latest['humidity']}%')
col3.metric("Condition", latest["weather_condition"])


st.markdown(f"<p style='font-size:14px;'>Recorded: {latest['recorded_at']} </p>", unsafe_allow_html=True)


st.dataframe(df_summary)


st.subheader("Average temperature by day")
st.line_chart(df_summary, x="date",y="avg_temp")