import streamlit as st
import pandas as pd
from scraper import fetch_bbc_india_news, dataframe_to_excel

st.set_page_config(page_title="News Scraper", page_icon="📰", layout="wide")

st.title("News Scraper")
st.write("Fetch latest headlines and summaries from BBC India and download them as CSV or Excel.")

if st.button("Scrape Latest News"):
    with st.spinner("Fetching news..."):
        df = fetch_bbc_india_news()
    if df.empty:
        st.error("No news items found. Please try again later.")
    else:
        st.success(f"Fetched {len(df)} news articles.")
        st.dataframe(df, use_container_width=True)
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download as CSV",
            data=csv_data,
            file_name="news_data.csv",
            mime="text/csv"
        )
        excel_buffer = dataframe_to_excel(df)
        st.download_button(
            "Download as Excel",
            data=excel_buffer.getvalue(),
            file_name="news_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Click the button above to scrape the latest BBC India news.")