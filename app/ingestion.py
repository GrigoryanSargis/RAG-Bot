from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

class DocumentIngestor:
    def __init__(self, db_path="data/faiss_index"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.db_path = db_path
        self.index = faiss.IndexFlatL2(384)  # Embedding size for MiniLM
        self.docs = []
        self._load()

    def _load(self):
        if os.path.exists(self.db_path + ".index") and os.path.exists(self.db_path + ".pkl"):
            self.index = faiss.read_index(self.db_path + ".index")
            with open(self.db_path + ".pkl", "rb") as f:
                self.docs = pickle.load(f)

    def _save(self):
        faiss.write_index(self.index, self.db_path + ".index")
        with open(self.db_path + ".pkl", "wb") as f:
            pickle.dump(self.docs, f)

    def is_concert_domain(self, text):
        keywords = [
            "concert", "live show", "world tour", "tour dates", "setlist", "performance schedule",
            "music tour", "headline tour", "support act", "touring", "music venue", "supporting artist",
            "stage", "festival lineup","tour", "guest appearance", "arena", "stadium", "on tour", "tour poster"
        ]
        text = text.lower()
        return sum(1 for kw in keywords if kw in text) >= 1

    def summarize(self, text):
        if len(text.split()) <= 10:
            return text.strip()  
        
        input_len = len(text.split())
        return self.summarizer(text, max_length=min(130,int(input_len * 0.6)), min_length=10, do_sample=False)[0]["summary_text"]


    def ingest(self, text):
        if not self.is_concert_domain(text):
            return "❌ Document rejected: Not related to concert tours."

        summary = self.summarize(text)
        embedding = self.embedder.encode([summary])
        self.index.add(embedding)
        self.docs.append(summary)
        self._save()
        return f"✅ Document accepted and ingested.\n Summary:\n{summary}"
