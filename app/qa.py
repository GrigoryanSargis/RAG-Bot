from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os
from online_search import search_concert_news

class QuestionAnsweringEngine:
    def __init__(self, db_path="data/faiss_index"):
        self.qa_model = pipeline("text2text-generation", model="google/flan-t5-small")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.db_path = db_path
        self.index = faiss.IndexFlatL2(384)
        self.docs = []
        self._load()

    def _load(self):
        if os.path.exists(self.db_path + ".index") and os.path.exists(self.db_path + ".pkl"):
            self.index = faiss.read_index(self.db_path + ".index")
            with open(self.db_path + ".pkl", "rb") as f:
                self.docs = pickle.load(f)

    def retrieve(self, query, top_k=3):
        if len(self.docs) == 0:
            return []
        query_vec = self.embedder.encode([query])
        _, indices = self.index.search(query_vec, top_k)
        return [self.docs[i] for i in indices[0] if i < len(self.docs)]

    def answer(self, query):
        retrieved_docs = self.retrieve(query)
        context = " ".join(retrieved_docs).strip()

        main_terms = [word.lower() for word in query.split() if word.lower() not in {"what", "where", "who", "when", "is", "are", "will", "do", "does", "did", "the", "a", "an", "in", "on", "to", "for"}]
        if not context or len(context.split()) < 10 or not any(term in context.lower() for term in main_terms):
            return "❌ No relevant documents found locally. Searching online...\n\n" + search_concert_news(query)

        input_text = f"Answer the question using only the context below and dont .\n\nContext:\n{context}\n\nQuestion:\n{query}"
        output = self.qa_model(input_text, max_length=100, do_sample=False)[0]["generated_text"]
        return output.strip()

