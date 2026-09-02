import io
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pypdf
import qrcode
import streamlit as st

st.set_page_config(
    page_title="Abdullah AI — Next Gen Intelligence",
    page_icon="⚡",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    .stApp {
        background: linear-gradient(135deg, #050508 0%, #0e1117 50%, #161b22 100%);
        font-family: 'Inter', sans-serif;
        color: #f0f6fc;
    }
    .hero-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ffa3, #00b4d8, #7928ca);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #8b949e;
        margin-bottom: 30px;
    }
    .glass-card {
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
  st.markdown("### 🌐 Панели Идоракунӣ")
  st.info(
      "**Abdullah AI v3.0**\n\nСистемаи зеҳни сунъӣ бо қобилияти таҳлили"
      " ҳуҷҷатҳо."
  )
  st.write("---")
  st.subheader("📱 QR Коди Барнома")
  app_url = st.text_input(
      "Линки барнома:", "https://abdullah-ai.streamlit.app"
  )
  if app_url:
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(app_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Скан кунед!", width=200)

st.markdown(
    "<h1 class='hero-title'>Abdullah AI</h1>", unsafe_allow_html=True
)
st.markdown(
    "<p class='hero-subtitle'>Зеҳни Сунъии Насли Нав • Сохташуда бо дасти Раис"
    " Абдуллоҳ</p>",
    unsafe_allow_html=True,
)

# Қисми боркунии PDF ва омодасозии пойгоҳи дониш
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("📂 Бор кардани китоб ё ҳуҷҷат (PDF Hub)")
uploaded_file = st.file_uploader(
    "Файли PDF-ро инҷо партоед:", type=["pdf"]
)

vectorstore = None
if uploaded_file is not None:
  with st.spinner("Китоб истодааст, ки таҳлил шавад... Лутфан каме сабр кунед."):
    reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
      text += page.extract_text() or ""

    # Қисм-қисм кардани матн барои модел
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    docs = text_splitter.split_text(text)

    # Сохтани векторҳо барои дарёфти ҷавоб
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma.from_texts(docs, embeddings)
    st.success(
        f"🎉 Китоб бомуваффақият хонда шуд! Шумораи саҳифаҳо:"
        f" {len(reader.pages)}. Акнун савол диҳед!"
    )
st.markdown("</div>", unsafe_allow_html=True)

# Қисми саволу ҷавоб аз китоб
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("💬 Пурсиш аз мундариҷаи китоб")
user_query = st.text_input(
    "Саволи худро дар бораи китоби боршуда нависед:",
    placeholder="Масалан: Дар ин китоб дар бораи чӣ гап меравад?",
)

if user_query:
  if vectorstore is not None:
    with st.spinner("Abdullah AI ҷавоб меҷӯяд..."):
      # Ёфтани қисми мувофиқи матн дар китоб
      results = vectorstore.similarity_search(user_query, k=3)
      context = "\n".join([doc.page_content for doc in results])

      st.markdown("---")
      st.success(f"**Саволи шумо:** {user_query}")
      st.markdown("### 🤖 Ҷавоби Abdullah AI аз китоб:")
      st.write(
          f"Дар асоси маводи китоби боршуда, маълумоти зерин ёфт шуд:\n\n{context}"
      )
  else:
    st.warning("⚠️ Аввал дар боло файли PDF-ро бор кунед, то аз он савол кунем!")
st.markdown("</div>", unsafe_allow_html=True)
