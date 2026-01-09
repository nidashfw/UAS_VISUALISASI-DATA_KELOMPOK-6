import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Cagar Budaya Jawa Barat",
    layout="wide"
)

# =========================
# TOGGLE MODE GELAP
# =========================
dark_mode = st.sidebar.toggle("🌙 Mode Gelap", value=False)

# =========================
# GOOGLE FONT & AESTHETIC CSS
# =========================
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {{
    font-family: 'Poppins', Poppins;
}}

/* ===== HILANGKAN GARIS PUTIH ===== */
hr {{
    display: none;
}}

/* ===== WARNA GLOBAL ===== */
:root {{
    --bg-main: {"#121212" if dark_mode else "#eef6f0"};
    --bg-soft: {"#1e1e1e" if dark_mode else "#ffffff"};
    --text-main: {"#eaeaea" if dark_mode else "#3f7f5f"};
    --text-soft: {"#cfcfcf" if dark_mode else "#4f6f5a"};
    --shadow-soft: 0 10px 25px rgba(0,0,0,0.08);
    --shadow-strong: 0 20px 45px rgba(0,0,0,0.25);
}}

/* ===== BACKGROUND ===== */
.stApp {{
    background: linear-gradient(135deg, var(--bg-main), {"#1c1c1c" if dark_mode else "#dfeee4"});
}}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {{
    background-color: {"#1c1c1c" if dark_mode else "#d8eadf"};
    border-right: 1px solid {"#333" if dark_mode else "#b7d3c2"};
}}

/* ===== SEMUA JUDUL TENGAH ===== */
h1, h2, h3 {{
    text-align: center !important;
    color: var(--text-main) !important;
}}

/* ===== JUDUL UTAMA ===== */
h1.main-title {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 10px;
}}

/* ===== SUBTITLE ===== */
.center-text {{
    color: var(--text-soft);
    margin-bottom: 35px;
    text-align: center;
}}

/* ===== CONTAINER TIMBUL ===== */
.elevated {{
    background: var(--bg-soft);
    padding: 0px;
    border-radius: 24px;
    box-shadow: var(--shadow-soft);
    margin-bottom: 30px;
    transition: all 0.35s ease;
}}

.elevated:hover {{
    transform: translateY(-6px);
    box-shadow: var(--shadow-strong);
}}

.elevated:active {{
    transform: translateY(-2px) scale(0.98);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {{
    width: 6px;
}}
::-webkit-scrollbar-thumb {{
    background: {"#555" if dark_mode else "#b7d3c2"};
    border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# JUDUL
# =========================
st.markdown('<h1 class="main-title">CAGAR BUDAYA JAWA BARAT</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="center-text">Visualisasi data cagar budaya berdasarkan <b>Kabupaten/Kota</b> dan <b>Jenis Cagar Budaya</b></p>',
    unsafe_allow_html=True
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv(
        "disparbud-od_20077_jml_cagar_budaya__jenis_kabupatenkota_v5_data.csv"
    )

df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔎 Filter Data")

selected_kabupaten = st.sidebar.multiselect(
    "Pilih Kabupaten/Kota",
    sorted(df["nama_kabupaten_kota"].unique()),
    default=sorted(df["nama_kabupaten_kota"].unique())
)

selected_jenis = st.sidebar.multiselect(
    "Pilih Jenis Cagar Budaya",
    sorted(df["jenis_cagar_budaya"].unique()),
    default=sorted(df["jenis_cagar_budaya"].unique())
)

filtered_df = df[
    (df["nama_kabupaten_kota"].isin(selected_kabupaten)) &
    (df["jenis_cagar_budaya"].isin(selected_jenis))
]

# =========================
# GRAFIK
# =========================
st.subheader("Grafik Jumlah Cagar Budaya")

grafik_df = filtered_df.groupby(
    "nama_kabupaten_kota", as_index=False
)["jumlah_cagar_budaya"].sum()

fig = px.bar(
    grafik_df,
    x="nama_kabupaten_kota",
    y="jumlah_cagar_budaya"
)

fig.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.markdown('<div class="elevated">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# MAP
# =========================
st.subheader("Peta Persebaran Cagar Budaya")

m = folium.Map(
    location=[-6.9, 107.6],
    zoom_start=8,
    tiles="CartoDB dark_matter" if dark_mode else "OpenStreetMap"
)

for _, row in grafik_df.iterrows():
    folium.CircleMarker(
        [-6.9, 107.6],
        radius=8,
        color="#6fbf8a",
        fill=True,
        fill_opacity=0.85,
        popup=f"<b>{row['nama_kabupaten_kota']}</b><br>Total: {row['jumlah_cagar_budaya']}"
    ).add_to(m)

st.markdown('<div class="elevated">', unsafe_allow_html=True)
st_folium(m, width=800, height=450)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABEL
# =========================
st.subheader("Data Detail")

st.markdown('<div class="elevated">', unsafe_allow_html=True)
st.dataframe(filtered_df)
st.markdown('</div>', unsafe_allow_html=True)
