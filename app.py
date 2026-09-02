import streamlit as st
import qrcode
from io import BytesIO
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Танзимоти саҳифаи барнома
st.set_page_config(
    page_title="Abdullah AI",
    page_icon="⚡",
    layout="centered"
# Дизайни махсус ва зебо (Gemini-like dark theme)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTitle {
        text-align: center;
        color: #00ffa3;
        font-family: 'Arial', sans-serif;
    }
    .stSubheader {
        text-align: center;
        color: #8ab4f8;
    }
    </style>
""", unsafe_allow_html=True)

# Сарлавҳаи барнома
st.markdown("<h1 class='stTitle'>Abdullah AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='stSubheader'>Зеҳни Сунъии Шахсӣ ва Ёвари Раис Абдуллоҳ</p>", unsafe_allow_html=True)
st.write("---")

# Майдон барои муошират бо зеҳни сунъӣ
user_query = st.text_input("Саволи худро ба Abdullah AI нависед:")

if user_query:
    st.success(f"Саволи шумо қабул шуд: {user_query}")
    st.write("🤖 Abdullah AI: Ман омодаам, ки ба шумо кӯмак расонам!")

# Қисми боркунии файлҳои PDF (барои кор бо ҳуҷҷатҳо)
st.write("---")
st.subheader("📂 Бор кардани ҳуҷҷатҳо ё китобҳо")
uploaded_file = st.file_uploader("Файли PDF-ро инҷо бор кунед:", type=["pdf"])

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    st.success(f"Фай бомуваффақият хонда шуд! Шумораи саҳифаҳо: {len(reader.pages)}")
