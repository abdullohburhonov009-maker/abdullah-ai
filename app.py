import io
import qrcode
import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

# Танзимоти саҳифа
st.set_page_config(
    page_title="Abdullah AI — Next Gen Intelligence",
    page_icon="⚡",
    layout="wide",
)

# Дизайни боҳашамат ва муосир (Gemini & Huawei style UI)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #050508 0%, #0e1117 50%, #161b22 100%);
        font-family: 'Inter', sans-serif;
        color: #f0f6fc;
    }
    
    /* Hero Title Styling */
    .hero-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ffa3, #00b4d8, #7928ca);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #8b949e;
        margin-bottom: 30px;
        font-weight: 300;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    /* Custom Sidebar QR Box */
    .qr-container {
        text-align: center;
        background: rgba(15, 20, 25, 0.8);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(0, 255, 163, 0.2);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar - Идоракунӣ ва QR Код
with st.sidebar:
  st.markdown("### 🌐 Панели Идоракунӣ")
  st.info(
      "**Abdullah AI v2.5**\n\nИн системаи шахсии Раис Абдуллоҳ аст, ки бо тарҳи пешрафта сохта шудааст."
  )

  st.write("---")
  st.subheader("📱 QR Коди Барнома")
  st.write(
      "Барои дар мактаб ё роҳ бо телефон кушодан, ин QR-ро скан кунед:"
  )

  # Гирифтани линки ҳозираи саҳифа ё гузоштани линки фармоишӣ
  app_url = st.text_input(
      "Линки барномаро инҷо монед:",
      "https://abdullah-ai.streamlit.app",
  )

  if app_url:
    # Сохтани QR код бо ёрӣ qrcode
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(app_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.image(byte_im, caption="Скан кунед ва дар телефон кушоед!", width=200)

# Қисми асосии саҳифа (Hero Section)
st.markdown(
    "<h1 class='hero-title'>Abdullah AI</h1>", unsafe_allow_html=True
)
st.markdown(
    "<p class='hero-subtitle'>Зеҳни Сунъии Насли Нав • Сохташуда бо дасти Раис"
    " Абдуллоҳ</p>",
    unsafe_allow_html=True,
)

# Ду колонна барои тарҳи моделҳои баландсуръат (Gemini/Huawei style)
col1, col2 = st.columns([2, 1])

with col1:
  st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
  st.subheader("💬 Муҳокима ва Пурсиш")
  user_query = st.text_input(
      "Саволи худро дар инҷо нависед...",
      placeholder="Масалан: Ба ман дар бораи барномасозӣ нақл кун...",
  )

  if user_query:
    st.markdown("---")
    st.success(f"**Савол:** {user_query}")
    st.markdown(
        "🤖 **Abdullah AI:** Ин як системаи хеле пуриқтидор аст. Ман дар"
        " хизмати Шумо ҳастам, Раис Абдуллоҳ! Ҳамаи супоришҳо бо беҳтарин сифат"
        " иҷро мешаванд."
    )
  st.markdown("</div>", unsafe_allow_html=True)

with col2:
  st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
  st.subheader("⚡ Ҳолати Система")
  st.metric(label="Суръати кор", value="99.9%", delta="Ultra Fast")
  st.metric(label="Амният", value="Encrypted", delta="Safe")
  st.markdown("</div>", unsafe_allow_html=True)

# Қисми боркунии ҳуҷҷатҳо (PDF Vector Hub)
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("📂 Пойгоҳи Ҳуҷҷатҳо ва Китобҳо (PDF Hub)")
uploaded_file = st.file_uploader(
    "Файли худро инҷо партоед (то 200MB роҳат қабул мешавад):", type=["pdf"]
)

if uploaded_file is not None:
  with st.spinner("Хондан ва коркарди китоб рафта истодааст..."):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
      text += page.extract_text() or ""
    st.success(
        f"🎉 Ҳуҷҷат бомуваффақият бор шуд! Шумораи саҳифаҳои китоб:"
        f" {len(reader.pages)}"
    )
    st.info("Китоб омодаи таҳлил ва саволу ҷавоб аст!")
st.markdown("</div>", unsafe_allow_html=True)
