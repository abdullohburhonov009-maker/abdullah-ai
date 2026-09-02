import os
import socket
import streamlit as st
import qrcode
from io import BytesIO
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Дизайна ва саҳифаи веб-сайт
st.set_page_config(page_title="Abdullah AI - Кӯмаки Зердасти Мактаб", page_icon="🤖", layout="centered")

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

st.title("🤖 Abdullah AI — Зеҳни Сунъии Раис Абдуллоҳ")
st.write("Ин барнома махсус аз тарафи **Раис Абдуллоҳ** сохта шудааст! Ҳамаи китобҳои таълимии соли 2025 ва Сираи Набавӣ дар ин ҷо ҳастанд.")

# Ҷойи нигоҳдории базаи китобҳо
DB_DIR = "vector_db"
BOOKS_DIR = "my_books"

@st.cache_resource
def load_and_vectorize_books():
    if not os.path.exists(BOOKS_DIR):
        os.makedirs(BOOKS_DIR)
        
    loader = PyPDFDirectoryLoader(BOOKS_DIR)
    docs = loader.load()
    
    if not docs:
        return None
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(splits, embeddings, persist_directory=DB_DIR)
    return vectordb

# Боргузории база
with st.spinner("Китобҳо хонда шуда истодаанд, лутфан каме сабр кунед..."):
    db = load_and_vectorize_books()

if db is None:
    st.warning("⚠️ Лутфан аввал китобҳои худро ба папкаи `my_books` партоед!")
else:
    # Ҷустуҷӯ ва саволу ҷавоб
    user_query = st.text_input("💬 Саволи худро нависед (масалан: 'Ман кистам?' ё савол аз китобҳо):")
    
    if user_query:
        # Санҷиш, агар Раис Абдуллоҳ дар бораи худ пурсад
        if "ман кистам" in user_query.lower() or "созандаи ту кӣ аст" in user_query.lower():
            st.markdown("### 🤖 Ҷавоби Abdullah AI:")
            st.success("Шумо Раис Абдуллоҳ ҳастед — созанда ва роҳбари ин зеҳни сунъӣ! Манро маҳз шумо сохтаед, Раиси азиз!")
        else:
            docs_and_scores = db.similarity_search_with_score(user_query, k=3)
            
            st.markdown("### 📖 Ҷавоб ва Сарчашмаҳо:")
            for i, (doc, score) in enumerate(docs_and_scores):
                source_file = os.path.basename(doc.metadata.get('source', 'Номаълум'))
                page_num = doc.metadata.get('page', 0) + 1
                
                st.info(f"**Ҷавоби {i+1}:**\n\n {doc.page_content}")
                st.markdown(f"🏷️ **Теги сарчашма:** `Китоб: {source_file} | Саҳифа: {page_num}`")
                st.divider()

# Қисми паҳлӯӣ ва QR-код барои телефон ва падарҷон
st.sidebar.title("📱 QR-коди Абдуллоҳ AI")
st.sidebar.write("Ин QR-кодро ба телефони падаратон фиристед, то барнома дар он ҷо низ кор кунад:")

# Гирифтани суроғаи IP-и компютер барои дар телефон кушода шудан
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
network_url = f"http://{local_ip}:8501"

# Сохтани QR-код аз рӯи суроғаи шабакавӣ
img = qrcode.make(network_url)
buf = BytesIO()
img.save(buf)
st.sidebar.image(buf.getvalue(), caption=f"Суроға: {network_url}", use_column_width=True)