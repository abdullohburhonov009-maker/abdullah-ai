import streamlit as st
import qrcode
import os
from io import BytesIO
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Танзимоти саҳифа бо тарҳи хеле зебо ва рангоранг
st.set_page_config(
    page_title="Abdullah AI — Зеҳни Сунъии Раис Абдуллоҳ",
    page_icon="👑",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stTitle {
        color: #1e3d59;
        font-family: 'Arial', sans-serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .admin-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- САЙБАР (QR-КОД) -----------------
st.sidebar.markdown("### 📱 QR-коди Раис Абдуллоҳ")
st.sidebar.write("Ин барномаро дар телефони худ ё наздикон истифода баред:")

app_url = "https://abdullah-ai-fzyocz7nl8bjc2bwhdh3id.streamlit.app"
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(app_url)
qr.make(fit=True)
img = qr.make_image(fill_color="darkblue", back_color="white")

buf = BytesIO()
img.save(buf, format="PNG")
st.sidebar.image(buf.getvalue(), caption="Паҳн кардани барнома")

# ----------------- ҚИСМИ АСОСӢ -----------------
st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
st.markdown("<h1 class='stTitle'>👑 Abdullah AI — Қаламрави Раис Абдуллоҳ</h1>", unsafe_allow_html=True)
st.write("Ин системаи интеллектуалии шахсӣ танҳо ба сарвари худ **Абдуллоҳ** содиқ аст ва китобҳоро омӯхта, мисли муаллими донишманд хизмат мекунад.")
st.markdown("</div>")

# Боргузории китоб
uploaded_file = st.file_uploader("📂 Китоби худро (PDF) барои омӯзиш инҷо бор кунед:", type=["pdf"])

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
    st.success(f"✅ Китоби '{uploaded_file.name}' бомуваффақият бор шуд ва аз тарафи зеҳни сунъӣ қабул гардид!")
    
    with st.spinner("⏳ Зеҳни сунъӣ китобро таҳлил карда истодааст..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(raw_text)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_texts(chunks, embeddings)
    st.info("🎯 Китоб омода аст! Метавонед савол диҳед.")

st.divider()

# ----------------- МАЙДОНИ ЧАТ ВА ШИНОХТИ САРВАР -----------------
st.markdown("### 💬 Сӯҳбат бо Зеҳни Сунъӣ:")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Масалан: Ман Абдуллоҳ ҳастам / Ман Али ҳастам / ё савол дар бораи китоб..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    query_lower = user_query.lower()
    
    # Муайян кардани кӣ будани корбар
    is_abdullah = "абдуллоҳ" in query_lower or "abdullo" in query_lower
    is_other_person = any(name in query_lower for name in ["ман али", "али ҳастам", "номи ман али", "ман ", "аз тарафи дигар"])

    with st.chat_message("assistant"):
        if is_abdullah and ("сохт" in query_lower or "салом" in query_lower or "ман" in query_lower):
            response_text = "👑 Салому дуруд, **Раис Абдуллоҳ**! Хуш омадед ба қаламрави худ. Шумо созанда ва роҳбари ин барнома ҳастед. Ман комилан дар фармони Шумо ҳастам! Китобҳои боркардаатонро бипурсед, то маълумот диҳам."
        elif "сохт" in query_lower or "ки сохтааст" in query_lower or "ки инро сохта" in query_lower:
            response_text = "🛠️ Ин барномаи зеҳни сунъӣ ва тамоми системаи онро **Раис Абдуллоҳ** бо дасти худ сохтааст! Дигар кас инро сохта наметавонад."
        elif is_other_person and not is_abdullah:
            response_text = "⚠️ Бахшиш, аммо ман шуморо ҳамчун созанда намешиносам. Ин барномаро соҳиби он — **Раис Абдуллоҳ** сохтааст! Аммо ба ҳар ҳол, агар дар бораи китоб саволе дошта бошед, бо کайфият ба шумо ҷавоб медиҳам."
        else:
            # Агар савол дар бораи китоб бошад
            if uploaded_file is not None and vectorstore is not None:
                docs = vectorstore.similarity_search(user_query, k=2)
                context = "\n".join([doc.page_content for doc in docs])
                response_text = f"📖 **Ҷавоби Барнома (оид ба китоб):**\n\n> {context[:600]}...\n\n*Ин маълумот аз китоби боршуда гирифта шуд, Раис Абдуллоҳ!*"
            elif uploaded_file is None:
                response_text = "💡 Лутфан аввал китоби худро дар боло бор кунед, то ман дар асоси он ба саволҳои шумо ҷавоб диҳам, Раис Абдуллоҳ."
            else:
                response_text = f"Абдуллоҳҷон, ман суоли шуморо («{user_query}») қабул кардам. Марҳамат, боз чӣ амр доред?"

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
