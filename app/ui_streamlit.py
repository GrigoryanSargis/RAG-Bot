import torch
import types
try:
    torch.classes.__path__ = types.SimpleNamespace(_path=[])
except Exception:
    pass

import streamlit as st
from ingestion import DocumentIngestor
from qa import QuestionAnsweringEngine

st.set_page_config(page_title="🎤 Concert Tour RAG Bot", layout="centered")
st.title("🎤 Concert Tour RAG Bot")
st.write("Upload concert tour documents and ask questions about 2025–2026 events.")

tab1, tab2 = st.tabs(["📄 Ingest Document", "❓ Ask Question"])

with tab1:
    uploaded_file = st.file_uploader("Upload a concert tour text file", type=["txt"])
    manual_text = st.text_area("Or paste concert tour information here")

    if uploaded_file:
        text = uploaded_file.read().decode("utf-8")
        ingestor = DocumentIngestor()
        result = ingestor.ingest(text)
        st.success(result if "✅" in result else result)

    elif manual_text.strip():
        ingestor = DocumentIngestor()
        result = ingestor.ingest(manual_text)
        st.success(result if "✅" in result else result)


with tab2:
    user_query = st.text_input("What do you want to know?")
    if user_query:
        engine = QuestionAnsweringEngine()
        answer = engine.answer(user_query)
        st.markdown("**Answer:**")
        st.write(answer)
