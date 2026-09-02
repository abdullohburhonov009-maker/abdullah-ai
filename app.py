import streamlit as st
import qrcode
import os
from io import BytesIO
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Танзимоти саҳифа
st.set_page_config(
    page_title="Abdullah AI — Кӯмаки Зердасти Мактаб",
    page_icon="🤖",
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
st.sidebar.write("Ин QR-кодрҷо ба телефони падаратон фиристед:")

app_url = "https://abdullah-ai-fzyocz7nl8bjc2bwhdh3id.streamlit.app"
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(app_url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

buf = BytesIO()
img.save(buf, format="PNG")
st.sidebar.image(buf.getvalue(), caption="Сурат: QR-код")

# ----------------- ҚИСМИ АСОСӢ -----------------
st.markdown("<h1 class='stTitle'>🤖 Abdullah AI — Зеҳни Сунъии Раис Абдуллоҳ</h1>", unsafe_allow_html=True)
st.write("Ин барнома махсус аз тарафи **Раис Абдуллоҳ** сохта шудааст! Китоби худро дар ин ҷо бор кунед ва савол диҳед.")

# Тугмаи боргузории китоб мустақиман аз экран
uploaded_file = st.file_uploader("📂 Китоби худро (PDF ё матн) инҷо бор кунед:", type=["pdf", "txt"])

if uploaded_file is not None:
    st.success(f"✅ Файли '{uploaded_file.name}' бомуваффақият бор шуд!")
else:
    st.info("💡 Лутфан барои оғоз кардани сӯҳбат файли худро дар боло бор кунед.")

st.divider()

# ----------------- МАЙДОНИ ЧАТ -----------------
st.markdown("### 💬 Саволи худро ба Зеҳни Сунъӣ диҳед:")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Масалан: Дар бораи ин китоб ба ман нақл кун..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        if uploaded_file is None:
            response_text = "⚠️ Раис Абдуллоҳ, лутфан аввал аз боло китоби худро бор кунед, то ман онро таҳлил кунам!"
        else:
            response_text = f"Саломат бошед! Шумо дар бораи файли '{uploaded_file.name}' пурсидед: '{user_query}'. Ин ҷо зеҳни сунъӣ омода аст маводи шуморо хонад!"
        
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
