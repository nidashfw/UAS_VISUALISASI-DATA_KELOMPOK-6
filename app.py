import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import os
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

image_map = {
    "KABUPATEN BOGOR": "images/kab_bogor.jpg",
    "KABUPATEN SUKABUMI": "images/kab_sukabumi.jpg",
    "KABUPATEN CIANJUR": "images/kab_cianjur.jpg",
    "KABUPATEN BANDUNG": "images/kab_bandung.jpg",
    "KABUPATEN GARUT": "images/kab_garut.jpg",
    "KABUPATEN TASIKMALAYA": "images/kab_tasikmalaya.jpg",
    "KABUPATEN CIAMIS": "images/kab_ciamis.jpg",
    "KABUPATEN KUNINGAN": "images/kab_kuningan.jpg",
    "KABUPATEN CIREBON": "images/kab_cirebon.jpg",
    "KABUPATEN MAJALENGKA": "images/kab_majalengka.jpg",
    "KABUPATEN SUMEDANG": "images/kab_sumedang.jpg",
    "KABUPATEN INDRAMAYU": "images/kab_indramayu.jpg",
    "KABUPATEN SUBANG": "images/kab_subang.jpg",
    "KABUPATEN PURWAKARTA": "images/kab_purwakarta.jpg",
    "KABUPATEN KARAWANG": "images/kab_karawang.jpg",
    "KABUPATEN BEKASI": "images/kab_bekasi.jpg",
    "KABUPATEN BANDUNG BARAT": "images/kab_bandung_barat.jpg",
    "KABUPATEN PANGANDARAN": "images/kab_pangandaran.jpg",
    "KOTA BOGOR": "images/kota_bogor.jpg",
    "KOTA SUKABUMI": "images/kota_sukabumi.jpg",
    "KOTA BANDUNG": "images/kota_bandung.jpg",
    "KOTA CIREBON": "images/kota_cirebon.jpg",
    "KOTA BEKASI": "images/kota_bekasi.jpg",
    "KOTA DEPOK": "images/kota_depok.jpg",
    "KOTA CIMAHI": "images/kota_cimahi.jpg",
    "KOTA TASIKMALAYA": "images/kota_tasikmalaya.jpg",
    "KOTA BANJAR": "images/kota_banjar.jpg",
}

place_map = {
    "KABUPATEN BOGOR": "Situs Cibalay (Kabupaten Bogor)",
    "KABUPATEN SUKABUMI": "Kampung Adat Ciptagelar (Kabupaten Sukabumi)",
    "KABUPATEN CIANJUR": "Bumi Ageung Cikidang (Kabupaten Cianjur)",
    "KABUPATEN BANDUNG": "Candi Bojong Menje (Kabupaten Bandung)",
    "KABUPATEN GARUT": "Candi Cangkuang (Kabupaten Garut)",
    "KABUPATEN TASIKMALAYA": "Kampung Naga (Kabupaten Tasikmalaya)",
    "KABUPATEN CIAMIS": "Situs Ciung Wanara Karangkamulyan (Kabupaten Ciamis)",
    "KABUPATEN KUNINGAN": "Paseban Tri Panca Tunggal (Kabupaten Kuningan)",
    "KABUPATEN CIREBON": "Keraton Kasepuhan (Kabupaten Cirebon)",
    "KABUPATEN MAJALENGKA": "Museum Talaga Manggung (Kabupaten Majalengka)",
    "KABUPATEN SUMEDANG": "Museum Prabu Geusan Ulun (Kabupaten Sumedang)",
    "KABUPATEN INDRAMAYU": "Situs Buyut Banjaran (Kabupaten Indramayu)",
    "KABUPATEN SUBANG": "Situs Cipari Subang (Kabupaten Subang)",
    "KABUPATEN PURWAKARTA": "Stasiun Purwakarta Lama (Kabupaten Purwakarta)",
    "KABUPATEN KARAWANG": "Situs Batujaya (Kabupaten Karawang)",
    "KABUPATEN BEKASI": "Gedung Juang Tambun (Kabupaten Bekasi)",
    "KABUPATEN BANDUNG BARAT": "Observatorium Bosscha (Kabupaten Bandung Barat)",
    "KABUPATEN PANGANDARAN": "Situs Batu Kalde (Kabupaten Pangandaran)",
    "KOTA BOGOR": "Istana Bogor (Kota Bogor)",
    "KOTA SUKABUMI": "Museum Pegadaian Sukabumi (Kota Sukabumi)",
    "KOTA BANDUNG": "Gedung Sate (Kota Bandung)",
    "KOTA CIREBON": "Keraton Kanoman (Kota Cirebon)",
    "KOTA BEKASI": "Gedung Juang 45 Bekasi (Kota Bekasi)",
    "KOTA DEPOK": "Rumah Cimanggis (Kota Depok)",
    "KOTA CIMAHI": "Gedung Sudirman Cimahi (Kota Cimahi)",
    "KOTA TASIKMALAYA": "Masjid Agung Tasikmalaya (Kota Tasikmalaya)",
    "KOTA BANJAR": "Situs Situ Leutik Banjar (Kota Banjar)"
}


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

st.subheader("Cagar Budaya Paling Populer Tiap Kabupaten/Kota")

cols = st.columns(4)
i = 0

for kab in selected_kabupaten:
    if kab in image_map:
        img_path = image_map[kab]
        place_name = place_map.get(kab, kab)

        if os.path.exists(img_path):
            with cols[i % 4]:
                st.image(img_path, width=230)
                st.markdown(
                    f"<p style='text-align:center; color:black; font-weight:600;'>{place_name}</p>",
                    unsafe_allow_html=True
                )
            i += 1


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
