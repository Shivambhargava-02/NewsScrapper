"""
NewsScope – News Search App
============================
This project has been upgraded to a full Streamlit web application.

▶  To launch the app, run:

    streamlit run app.py

Then open  http://localhost:8501  in your browser.

Features:
  • Search bar for any news topic
  • 10 category quick-buttons (Tech, Sports, Health, etc.)
  • Real-time articles via NewsAPI or Google News RSS (BeautifulSoup fallback)
  • Dark, premium UI with article cards, images & direct links

Optional: add your free NewsAPI key to a .env file
  (copy .env.example → .env and fill in NEWS_API_KEY)
"""

import subprocess
import sys

if __name__ == "__main__":
    print("Launching NewsScope Streamlit app...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
