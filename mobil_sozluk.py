import streamlit as st
import random
import os
import pandas as pd

from redis_ekle import kelime_ekle
from redis_sil import kelime_sil
from redis_listele import tum_kelimeleri_getir

# Sayfa ayarı (en üste gelmeli!)
st.set_page_config(page_title="İngilizce-Türkçe Sözlük", layout="centered")

# Tema stili
st.markdown("""
    <style>
    /* Genel Arka Plan */
    body {
        background-color: #f5f5f5;
    }

    /* Tüm yazı tipleri */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #333333;
        transition: all 0.3s ease-in-out;
    }

    /* Başlıklar */
    h1, h2, h3 {
        color: #222222;
    }

    /* Butonlar */
    .stButton>button {
        background: linear-gradient(to right, #4a90e2, #6fb1fc);
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 10px;
        transition: background 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background: linear-gradient(to right, #357ABD, #5794e0);
    }

    /* Giriş alanları */
    input, textarea, .stTextInput>div>div>input {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 0.5em;
        transition: border 0.3s ease-in-out;
    }

    input:focus, textarea:focus {
        border: 1px solid #4a90e2;
    }

    /* Veri tablosu */
    .stDataFrame {
        border-radius: 10px;
        background-color: #ffffff;
    }

    /* Kenar çubuğu başlığı */
    .css-1d391kg { 
        color: #222222;
    }

    /* Alt footer yazısını gizle (Streamlit logosu) */
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# Sayfa seçici
sayfa = st.sidebar.selectbox("📂 Sayfa Seçiniz", ["🏠 Ana Sayfa", "📖 Sözlük", "📝 Quiz Modu", "📜 Sözlük Listesi"])

# 🏠 Ana Sayfa
if sayfa == "🏠 Ana Sayfa":
    st.markdown("## 📚 İngilizce-Türkçe Sözlük")
    st.markdown("Bu site ile kelime arayabilir, yeni kelime ekleyebilir veya Quiz modunda kendinizi test edebilirsiniz.")

# 📖 Sözlük Sayfası
elif sayfa == "📖 Sözlük":
    st.subheader("🔍 Kelime Ara")
    kelime = st.text_input("Kelime giriniz:")

    sozluk = tum_kelimeleri_getir()
    ters_sozluk = {v: k for k, v in sozluk.items()}

    if st.button("Ara"):
        anlam = sozluk.get(kelime.capitalize(), ters_sozluk.get(kelime.capitalize(), "Kelime bulunamadı.")) 
        st.success(f"**{kelime.capitalize()} ➜ {anlam}**")

    st.subheader("➕ Yeni Kelime Ekle")
    yeni_kelime = st.text_input("Yeni Kelime:")
    yeni_anlam = st.text_input("Anlamı:")

    if st.button("Ekle"):
        if yeni_kelime and yeni_anlam:
            kelime_ekle(yeni_kelime, yeni_anlam)
            st.success(f"✅ '{yeni_kelime.capitalize()}' eklenmiştir.")

    st.subheader("🗑️ Kelime Sil")
    sil_kelime = st.text_input("Silinecek Kelime:")
    if st.button("Sil"):
        sonuc = kelime_sil(sil_kelime)
        if sonuc == 1:
            st.warning(f"❌ '{sil_kelime.capitalize()}' silinmiştir.")
        else:
            st.error("Kelime bulunamadı.")

# 📝 Quiz Modu 
elif sayfa == "📝 Quiz Modu":
    st.subheader("🧠 Quiz Modu")
    sozluk = tum_kelimeleri_getir()
    ters_sozluk = {v: k for k, v in sozluk.items()}

    if "quiz_kelime" not in st.session_state:
        st.session_state.quiz_kelime = ""
        st.session_state.quiz_cevap = ""
        st.session_state.soru_tipi = ""
        st.session_state.sec_option = ""

    def yeni_soru():
        if random.choice([True, False]):
            st.session_state.soru_tipi = "ing-tr"
            st.session_state.quiz_kelime, st.session_state.quiz_cevap = random.choice(list(sozluk.items()))
            secenekler = random.sample(list(sozluk.values()), 4)
        else:
            st.session_state.soru_tipi = "tr-ing"
            st.session_state.quiz_kelime, st.session_state.quiz_cevap = random.choice(list(ters_sozluk.items()))
            secenekler = random.sample(list(ters_sozluk.values()), 4)

        if st.session_state.quiz_cevap not in secenekler:
            secenekler[random.randint(0, 3)] = st.session_state.quiz_cevap

        random.shuffle(secenekler)
        st.session_state.sec_options = secenekler

    if st.button("🔄 Yeni Soru"):
        yeni_soru()

    if st.session_state.quiz_kelime:
        st.markdown(f"**❓ {st.session_state.quiz_kelime} ne anlama gelir?**")
        for secenek in st.session_state.sec_options:
            if st.button(secenek):
                if secenek == st.session_state.quiz_cevap:
                    st.success("✅ Doğru!")
                else:
                    st.error(f"❌ Yanlış! Doğru cevap: {st.session_state.quiz_cevap}")
                    st.session_state.quiz_kelime = ""

# 📜 Sözlük Listesi Sayfası

if sayfa == "📜 Sözlük Listesi":
    st.header("📜 Tüm Sözlük Listesi")
    sozluk = tum_kelimeleri_getir()

    if sozluk:
        df = pd.DataFrame(sozluk.items(), columns=["Kelime", "Anlam"])
        df.index += 1
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Henüz sözlükte kayıtlı kelime yok.")