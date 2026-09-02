import io
import os
import qrcode
import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

# Танзимоти саҳифа
st.set_page_config(
    page_title="Abdullah AI — Multi-Library Intelligence",
    page_icon="⚡",
    layout="wide",
)

# Дизайни боҳашамат (Gemini & Huawei style UI)
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
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ffa3, #00b4d8, #7928ca);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #8b949e;
        margin-bottom: 25px;
        font-weight: 300;
    }

    .glass-card {
        background: rgba(22, 27, 34, 0.75);
        backdrop-filter: blur(14px);
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

# Панели канори бо QR Код
with st.sidebar:
  st.markdown("### 🌐 Панели Идоракунӣ")
  st.info(
      "**Abdullah AI v5.0**\n\nСистемаи дастгирии ҳамзамони чанд китоб ва ҳуҷҷат."
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
    st.image(buf.getvalue(), caption="Скан кунед ва дар телефон кушоед!", width=200)

# Сарлавҳаи асосӣ
st.markdown(
    "<h1 class='hero-title'>Abdullah AI</h1>", unsafe_allow_html=True
)
st.markdown(
    "<p class='hero-subtitle'>Зеҳни Сунъии кушодаи чандкитоба • Сохташуда бо дасти"
    " Раис Абдуллоҳ</p>",
    unsafe_allow_html=True,
)

# 1. Қисми боркунии чанд китоб ҳамзамон (Multi-PDF Hub)
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("📂 1. Боркунии якбораи чанд Китоб ё Ҳуҷҷат")
st.write(
    "Метавонед якбора якчанд файли PDF-ро аз компютер интихоб карда партоед"
    " (система ҳамаашро якҷоя мехонад):"
)

# Илова шудани accept_multiple_files=True барои қабули чанд файл ҳамзамон
uploaded_files = st.file_uploader(
    "Файлҳои PDF-ро инҷо интихоб кунед:", type=["pdf"], accept_multiple_files=True
)

vectorstore = None
if uploaded_files:
  with st.spinner(
      "⚡ Китобҳо бо суръати баланд хонда ва индекс шуда истодаанд..."
  ):
    all_texts = []
    total_pages = 0

    # Давра барои хондани ҳар як файли боршуда
    for uploaded_file in uploaded_files:
      reader = PdfReader(uploaded_file)
      total_pages += len(reader.pages)
      file_text = ""
      for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
          file_text += f"\n[Китоб: {uploaded_file.name} | Саҳифа {i+1}]\n" + page_text
      all_texts.append(file_text)

    combined_text = "\n".join(all_texts)

    # Қисм-қисм кардани матни ҳамаи китобҳо
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=80
    )
    docs = text_splitter.split_text(combined_text)

    # Сохтани хотираи векторӣ барои ҳамаи китобҳо якҷоя
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma.from_texts(docs, embeddings)

    st.success(
        f"🎉 Ҳамаи китобҳо ({len(uploaded_files)} адад) бомуваффақият хонда"
        f" шуданд! Шумораи умумии саҳифаҳо: {total_pages}. Акнун модел омодаи"
        " ҷавоб додан аст!"
    )
st.markdown("</div>", unsafe_allow_html=True)

# 2. Қисми саволу ҷавоб аз байни ҳамаи китобҳо
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("💬 2. Пурсиш аз маҷмӯи китобҳо (Мисли тир)")
user_query = st.text_input(
    "Саволи худро дар бораи китобҳои боршуда нависед:",
    placeholder="Масалан: Дар байни ин китобҳо дар бораи фалон мавзӯъ чӣ гуфта"
    " шудааст?",
)

if user_query:
  if vectorstore is not None:
    with st.spinner("🤖 Abdullah AI дар байни китобҳо мегардад..."):
      # Ҷустуҷӯи фаврӣ дар байни ҳамаи китобҳо
      results = vectorstore.similarity_search(user_query, k=4)
      context_text = "\n\n".join([doc.page_content for doc in results])

      st.markdown("---")
      st.markdown(f"**❓ Саволи шумо:** {user_query}")
      st.markdown("### ⚡ Ҷавоби фаврии Abdullah AI аз китобҳо:")

      st.info(
          "Дар асоси таҳлили китобҳои боршуда, маълумоти марбута чунин"
          f" аст:\n\n{context_text}"
      )
      st.success("✨ Ҷавоб бо суръати баланд аз маҷмӯи китобҳо ёфт шуд!")
  else:
    st.warning(
        "⚠️ Лутфан аввал дар боло файлҳои PDF-ро бор кунед, то система онҳоро"
        " бихонад!"
    )
st.markdown("</div>", unsafe_allow_html=True)
