import streamlit as st
import qrcode
import os
from io import BytesIO
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Дизайн ва танзимоти саҳифаи веб-сайт
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
    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- САЙБАР (QR-КОД) -----------------
st.sidebar.markdown("### 📱 QR-коди Абдуллоҳ AI")
st.sidebar.write("Ин QR-кодрҷо ба телефони падаратон фиристед, то барнома дар он ҷо низ кор кунад:")

# Сохтани QR-код бо истиноди барнома
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
st.write("Ин барнома махсус аз тарафи **Раис Абдуллоҳ** сохта шудааст! Ҳамаи китобҳои таълимии соли 2025 ва Сираи Набавӣ дар ин ҷо ҳастанд.")

# Тафтиши папкаи китобҳо
books_dir = "my_books"
if not os.path.exists(books_dir):
    os.makedirs(books_dir)

# Огоҳӣ агар папка холӣ бошад
files = os.listdir(books_dir)
if not files:
    st.warning("⚠️ Лутфан аввал китобҳои худро ба папкаи `my_books` дар GitHub партоед!")
else:
    st.success(f"✅ Китобҳо ёфт шуданд! Шумораи файлҳо: {len(files)}")

st.divider()

# ----------------- МАЙДОНИ ЧАТ ВА САВОЛУ ҶАВОБ -----------------
st.markdown("### 💬 Саволи худро ба Зеҳни Сунъӣ диҳед:")

# Нигоҳ доштани таърихи чат дар сессия
if "messages" not in st.session_state:
    st.session_state.messages = []

# Нишон додани паёмҳои пешина
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Қабули саволи нав аз корбар
if user_query := st.chat_input("Масалан: Дар китоб дар бораи чӣ гуфта шудааст?"):
    # Саволи корбарро дар экран мемонем
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Ҷавоби сунъӣ (AI Response)
    with st.chat_message("assistant"):
        response_text = f"Саломат бошед, Раис Абдуллоҳ! Шумо пурсидед: '{user_query}'. Ин савол аз китобҳои таълимии شما тафтиш шуда истодааст..."
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
