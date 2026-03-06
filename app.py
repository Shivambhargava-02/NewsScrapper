import streamlit as st
<<<<<<< HEAD
import os
import html as html_mod
from dotenv import load_dotenv
from scraper.news_fetcher import get_news

# ── Load .env if present ──────────────────────────────────────────────────────
load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NewsScope – Search Any News",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS: dark premium theme ────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- Google Fonts ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ---------- Global reset ---------- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---------- Main background ---------- */
.stApp {
    background: #0d0f14;
    color: #e2e8f0;
}

/* ---------- Hero header ---------- */
.hero {
    background: linear-gradient(135deg, #1a1c2e 0%, #0f3460 40%, #16213e 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    border: 1px solid rgba(99,179,237,0.15);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; right: -40px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(159,122,234,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 3.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #63b3ed, #9f7aea, #f687b3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -1px;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-top: 0.5rem;
    font-weight: 300;
}

/* ---------- Search bar ---------- */
.stTextInput > div > div > input {
    background: #1e2130 !important;
    border: 2px solid #2d3748 !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #63b3ed !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.18) !important;
}

/* ---------- Buttons ---------- */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: none !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
}
/* Search / primary button */
.primary-btn > button {
    background: linear-gradient(135deg, #63b3ed, #9f7aea) !important;
    color: white !important;
    padding: 0.7rem 2rem !important;
    box-shadow: 0 4px 20px rgba(99,179,237,0.3) !important;
}
.primary-btn > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99,179,237,0.45) !important;
}
/* Category chips */
.stButton > button {
    background: #1e2130 !important;
    color: #94a3b8 !important;
    border: 1.5px solid #2d3748 !important;
    padding: 0.45rem 1rem !important;
}
.stButton > button:hover {
    background: #2d3748 !important;
    color: #e2e8f0 !important;
    border-color: #63b3ed !important;
    transform: translateY(-1px) !important;
}

.card-wrapper {
    display: block;
    text-decoration: none;
    color: inherit;
    margin-bottom: 1.2rem;
}
.card-wrapper:hover .card {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.5);
    border-color: #2d4a7a;
}
.card-wrapper:hover .card::before {
    opacity: 1;
}
/* ---------- Article cards ---------- */
.card {
    background: linear-gradient(145deg, #1a1d2e, #161929);
    border: 1px solid #1e2640;
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #63b3ed, #9f7aea);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.5);
    border-color: #2d4a7a;
}
.card:hover::before {
    opacity: 1;
}
.card-source {
    display: inline-block;
    background: rgba(99,179,237,0.15);
    color: #63b3ed;
    border-radius: 8px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}
.card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2e8f0;
    line-height: 1.45;
    margin-bottom: 0.6rem;
}
.card-desc {
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.65;
    margin-bottom: 1rem;
    font-weight: 400;
}
.card-date {
    font-size: 0.78rem;
    color: #4a5568;
    margin-bottom: 0.8rem;
}
.card-img {
    width: 100%;
    border-radius: 10px;
    margin-bottom: 0.9rem;
    max-height: 180px;
    object-fit: cover;
}
.open-hint {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #9f7aea;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    margin-top: auto;
    padding-top: 0.5rem;
    border-top: 1px solid #1e2640;
    width: 100%;
}
.card-wrapper:hover .open-hint {
    color: #f687b3;
}

/* ---------- Divider ---------- */
hr { border-color: #1e2640 !important; }

/* ---------- Badge / pill ---------- */
.badge {
    display: inline-block;
    background: rgba(159,122,234,0.15);
    color: #9f7aea;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
}

/* ---------- Stats row ---------- */
.stats {
    font-size: 0.85rem;
    color: #4a5568;
    margin-bottom: 1.5rem;
}

/* ---------- No-results ---------- */
.no-result {
    text-align: center;
    padding: 4rem 2rem;
    color: #4a5568;
}
.no-result-icon { font-size: 4rem; margin-bottom: 1rem; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: #13151f !important;
    border-right: 1px solid #1e2640;
}

/* ---------- Streamlit overrides ---------- */
.block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Categories ────────────────────────────────────────────────────────────────
CATEGORIES = {
    "🔬 Science":        "science",
    "💻 Technology":     "technology",
    "💰 Business":       "business",
    "⚽ Sports":         "sports",
    "🎬 Entertainment":  "entertainment",
    "🏥 Health":         "health",
    "🌍 World":          "world news",
    "🚀 Space":          "space",
    "🎮 Gaming":         "gaming",
    "🌿 Environment":    "climate environment",
}

# ── Session state initialisation ─────────────────────────────────────────────
if "query" not in st.session_state:
    st.session_state["query"] = ""
if "articles" not in st.session_state:
    st.session_state["articles"] = []
if "source_label" not in st.session_state:
    st.session_state["source_label"] = ""
if "searched" not in st.session_state:
    st.session_state["searched"] = False


# ── Sidebar: API key & settings ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    sidebar_key = st.text_input(
        "🔑 NewsAPI Key (optional)",
        type="password",
        placeholder="Paste key for higher limits",
        help="Get a free key at newsapi.org. Without it, the app uses Google News RSS.",
    )

    num_results = st.slider("📄 Number of results", min_value=5, max_value=30, value=12, step=1)

    st.markdown("---")
    st.markdown("""
    **About**
    
    This app fetches real-time news using:
    - **NewsAPI** (with API key)
    - **Google News RSS** (fallback, no key needed)
    
    Built with `requests`, `BeautifulSoup` & `Streamlit`.
    """)
    st.markdown("[Get free NewsAPI key →](https://newsapi.org)")


# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <p class="hero-title">📰 NewsScope</p>
  <p class="hero-subtitle">Search real-time news on any topic — powered by NewsAPI &amp; BeautifulSoup</p>
</div>
""", unsafe_allow_html=True)


# ── Search bar ────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    search_input = st.text_input(
        label="search_bar",
        label_visibility="collapsed",
        placeholder="🔍  Search for any topic… e.g. cricket, AI, elections, Tesla",
        value=st.session_state["query"],
        key="search_text",
    )

with col_btn:
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    search_clicked = st.button("Search", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ── Category quick-buttons ────────────────────────────────────────────────────
st.markdown("#### Browse by Category")
cat_cols = st.columns(len(CATEGORIES))
selected_category = None
for i, (label, query_val) in enumerate(CATEGORIES.items()):
    with cat_cols[i]:
        if st.button(label, use_container_width=True, key=f"cat_{i}"):
            selected_category = query_val

st.markdown("---")


# ── Trigger search ────────────────────────────────────────────────────────────
final_query = None

if search_clicked and search_input.strip():
    final_query = search_input.strip()

if selected_category:
    final_query = selected_category

if final_query:
    st.session_state["query"] = final_query
    api_key = sidebar_key.strip() if sidebar_key else os.getenv("NEWS_API_KEY", "")
    with st.spinner(f'Fetching news for **"{final_query}"**…'):
        articles, source_label = get_news(final_query, api_key=api_key, page_size=num_results)
    st.session_state["articles"] = articles
    st.session_state["source_label"] = source_label
    st.session_state["searched"] = True


# ── Display articles ──────────────────────────────────────────────────────────
if st.session_state["searched"]:
    articles     = st.session_state["articles"]
    source_label = st.session_state["source_label"]
    current_q    = st.session_state["query"]

    if articles:
        st.markdown(
            f'<p class="stats">Found <strong>{len(articles)}</strong> articles for '
            f'"<em>{current_q}</em>" &nbsp;·&nbsp; '
            f'<span class="badge">{source_label}</span></p>',
            unsafe_allow_html=True,
        )

        # 2-column grid
        for i in range(0, len(articles), 2):
            row_cols = st.columns(2)
            for j, col in enumerate(row_cols):
                idx = i + j
                if idx >= len(articles):
                    break
                art = articles[idx]
                with col:
                    # HTML-escape ALL text to prevent RSS HTML from breaking card layout
                    safe_title  = html_mod.escape(art['title'])
                    safe_source = html_mod.escape(art['source'])
                    safe_desc   = html_mod.escape(art['description'])
                    safe_date   = html_mod.escape(art['published'])
                    safe_url    = art['url']  # URL must not be escaped

                    # Build image HTML
                    img_html = ""
                    if art.get("image"):
                        img_html = f'<img class="card-img" src="{art["image"]}" alt="article image" onerror="this.style.display=\'none\'"/>'

                    card_html = f"""
                    <a class="card-wrapper" href="{safe_url}" target="_blank" rel="noopener noreferrer">
                      <div class="card">
                        {img_html}
                        <div class="card-source">{safe_source}</div>
                        <div class="card-title">{safe_title}</div>
                        <div class="card-date">🕐 {safe_date}</div>
                        <div class="card-desc">{safe_desc}</div>
                        <div class="open-hint">🔗 Click to open full article &nbsp;→</div>
                      </div>
                    </a>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="no-result">
            <div class="no-result-icon">🔭</div>
            <h3>No articles found</h3>
            <p>Try a different keyword or check your internet connection.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Welcome state — show trending placeholder cards
    st.markdown("""
    <div class="no-result">
        <div class="no-result-icon">📰</div>
        <h3 style="color:#e2e8f0;">Ready to Explore the World's News?</h3>
        <p>Type a topic in the search bar above or click a category button to get started.</p>
    </div>
    """, unsafe_allow_html=True)
=======
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
>>>>>>> 51cbd346f0cdf485a474ee917168ef89ce10b784
