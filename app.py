import streamlit as st
import qrcode
import os
from io import BytesIO
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Танзимоти саҳифа
st.set_page_config(
    page_title="Abdullah AI — Омӯзгори Ракқами",
    page_icon="👨‍🏫",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTitle {
        color: #1e3d59;
        font-family: 'Arial', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- САЙБАР (QR-КОД) -----------------
st.sidebar.markdown("### 📱 QR-коди Абдуллоҳ AI")
st.sidebar.write("Ин барномаро дар телефон низ истифода баред:")

app_url = "https://abdullah-ai-fzyocz7nl8bjc2bwhdh3id.streamlit.app"
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(app_url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

buf = BytesIO()
img.save(buf, format="PNG")
st.sidebar.image(buf.getvalue(), caption="Сурат: QR-код")

# ----------------- ҚИСМИ АСОСӢ -----------------
st.markdown("<h1 class='stTitle'>👨‍🏫 Abdullah AI — Омӯзгори Раис Абдуллоҳ</h1>", unsafe_allow_html=True)
st.write("Салом, Раис Абдуллоҳ! Ин барнома ҳамчун муаллими шахсии шумо китоби боршударо мехонад ва ба саволҳои шумо ҷавоб медиҳад.")

# Боргузории файл
uploaded_file = st.file_uploader("📂 Китоби худро (PDF) инҷо бор кунед:", type=["pdf"])

# Функция барои хондани матни PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# Коркарди китоб агар бор шуда бошад
vectorstore = None
if uploaded_file is not None:
    st.success(f"✅ Файли '{uploaded_file.name}' бомуваффақият бор шуд ва аз тарафи муаллим қабул гардид!")
    
    with st.spinner("⏳ Муаллим китобро хонда истодааст, лутфан каме сабр кунед..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        
        # Тақсим кардани матн ба қисмҳо
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(raw_text)
        
        # Сохтани эмбеддингҳо
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_texts(chunks, embeddings)
    st.info("🎯 Китоб комилан хонда шуд! Акнун метавонед ҳар суоле доред бипурсед.")

st.divider()

# ----------------- МАЙДОНИ ЧАТ (ОМӮЗГОР) -----------------
st.markdown("### 💬 Саволи худро ба Муаллим диҳед:")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Масалан: Ин китоб дар бораи чӣ аст? Қоидаи асосиро фаҳмон."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        if uploaded_file is None:
            response_text = "⚠️ Раис Абдуллоҳ, лутфан аввал аз боло китоби худро бор кунед, то муаллим онро хонда тавонад!"
        else:
            if vectorstore is not None:
                # Ҷустуҷӯ дар хотираи китоб
                docs = vectorstore.similarity_search(user_query, k=2)
                context = "\n".join([doc.page_content for doc in docs])
                
                # Ҷавоби муаллимона
                response_text = f"**Ҷавоби Муаллим:**\n\nБарои саволи шумо («{user_query}»), аз китоб ин маълумот ёфт шуд:\n\n> {context[:600]}...\n\n*Умедворам ин ба шумо фаҳмо буд, Раис Абдуллоҳ! Агар боз савол доред, марҳамат бипурсед.*"
            else:
                response_text = "ХАТОГИ: Китоб ҳанӯз коркард нашудааст."
        
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
