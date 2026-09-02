import streamlit as st
import qrcode
from io import BytesIO
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Танзимоти саҳифа бо тарҳи замонавӣ ва шоҳона
st.set_page_config(
    page_title="Abdullah AI — Зеҳни Сунъии Шахсӣ",
    page_icon="👑",
    layout="centered"
# Дизайни босифат ва махсус бо CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stTitle {
        color: #1e3d59;
        font-family: 'Arial', sans-serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        text-align: center;
    }
    .admin-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 6px solid #1e3d59;
    }
    .owner-badge {
        background: linear-gradient(45deg, #ff4b4b, #ff8f00);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- САЙБАР (МЕНЮИ РАИС АБДУЛЛОҲ) -----------------
st.sidebar.markdown("### 👑 Менюи Идоракунӣ")
st.sidebar.markdown("<div class='owner-badge'>Созанда: Абдуллоҳ Ҳайдар</div>", unsafe_allow_html=True)
st.sidebar.write("Ин барномаи шахсии шумост. Бо скан кардани QR-код метавонед онро дар телефон низ истифода баред:")

# Линки доимии барномаи ту
app_url = "https://abdullah-ai-fzyocz7nl8bjc2bwhdh3id.streamlit.app"

# Сохтани QR-коди худкор ва зебо
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(app_url)
qr.make(fit=True)
img = qr.make_image(fill_color="#1e3d59", back_color="white")

buf = BytesIO()
img.save(buf, format="PNG")
st.sidebar.image(buf.getvalue(), caption="📱 QR-коди мустақими барнома")

st.sidebar.divider()
st.sidebar.markdown("### ℹ️ Маълумот")
st.sidebar.write("Барномаи RAG AI бо ёрии LangChain, ChromaDB ва HuggingFace сохта шудааст.")

# ----------------- ҚИСМИ АСОСӢ -----------------
st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
st.markdown("<h1 class='stTitle'>👑 Abdullah & Haydar AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #555;'>Хуш омадед ба системаи интеллектуалии шахсии худ, <b>Раис Абдуллоҳ</b>!</p>", unsafe_allow_html=True)
st.markdown("</div>")

# Қисми боргузории китоб
st.markdown("### 📚 Боргузории Китоб барои Таҳлил")
uploaded_file = st.file_uploader("📂 Китоби худро (PDF) инҷо ворид кунед:", type=["pdf"])

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

vectorstore = None
if uploaded_file is not None:
    st.markdown(f"""
        <div class='success-box'>
            <b>✅ Китоби '{uploaded_file.name}' бомуваффақият бор шуд!</b><br>
            Муаллими сунъӣ матни китобро хонда истодааст...
        </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("⏳ Лутфан каме сабр кунед, зеҳни сунъӣ маълумотро коркард дорад..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(raw_text)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_texts(chunks, embeddings)
    st.success("🎯 Китоб комилан омода аст! Акнун метавонед ҳар суоле доред бипурсед.")

st.divider()

# ----------------- СӮҲБАТ БО МУАЛЛИМИ СУНЪӢ -----------------
st.markdown("### 💬 Сӯҳбат бо Муаллим ва Низоми Шинохти Сарвар")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Масалан: Ман Абдуллоҳ Ҳайдар ҳастам / Ин китоб дар бораи чӣ аст?"):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    query_lower = user_query.lower()
    
    is_abdullah = "абдуллоҳ" in query_lower or "abdullo" in query_lower or "хайдар" in query_lower or "раис" in query_lower
    is_other_person = any(name in query_lower for name in ["ман али", "али ҳастам", "номи ман али", "ман ", "дигар кас"])

    with st.chat_message("assistant"):
        if is_abdullah and ("сохт" in query_lower or "салом" in query_lower or "ман" in query_lower):
            response_text = "👑 Салому дуруд, **Раис Абдуллоҳ Ҳайдар**! Шумо созанда ва роҳбари ягонаи ин барнома ҳастед. Ман бо камоли минат дар фармони Шумо ҳастам! Саволҳои худро аз китоби боршуда диҳед."
        elif "сохт" in query_lower or "ки сохтааст" in query_lower or "ки инро сохта" in query_lower:
            response_text = "🛠️ Ин барномаи зеҳни сунъӣ ва тамоми сохтори онро бо дасти худ сарвари мо — **Раис Абдуллоҳ Ҳайдар** сохтааст!"
        elif is_other_person and not is_abdullah:
            response_text = "⚠️ Бахшиш, аммо созандаи ин система фақат ва фақат **Раис Абдуллоҳ Ҳайдар** аст! Ман фармонҳои ӯро иҷро мекунам, лекин ба ҳар ҳол ба саволҳои китоби шумо бо эҳтиром ҷавоб медиҳам."
        else:
            if uploaded_file is not None and vectorstore is not None:
                docs = vectorstore.similarity_search(user_query, k=2)
                context = "\n".join([doc.page_content for doc in docs])
                response_text = f"📖 **Ҷавоби Муаллим:**\n\n> {context[:600]}...\n\n*Ин маълумот аз китоби шумо гирифта шуд, Раис Абдуллоҳ!*"
            elif uploaded_file is None:
                response_text = "💡 Лутфан аввал китоби худро дар боло бор кунед, то муаллим онро хонда диҳад, Раис Абдуллоҳ."
            else:
                response_text = f"Абдуллоҳҷон, суоли шуморо қабул кардам. Марҳамат, боз чӣ амр доред?"

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
