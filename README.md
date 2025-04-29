# 🎤 Concert Tour RAG Bot

The system uses a **Retrieval-Augmented Generation (RAG)** architecture to ingest tour-related documents, summarize them (if needed), and answer user questions **strictly based on ingested content**. If the answer is not available locally, it will optionally fall back to an online search.

---

## ✅ Features

- 📄 **Document Ingestion** (text or file)
  - Relevance check for concert/tour topics
  - Summarization for long documents (LLM-based)
  - Skips summarization for short inputs to avoid hallucination
  - Stores summaries in a FAISS vector DB

- ❓ **Question Answering**
  - Semantic search over ingested docs
  - Answer generation via `flan-t5-small`
  - Smart filtering of irrelevant matches
  - Optional fallback to DuckDuckGo for online search

- 🖼️ **Streamlit UI** *(Bonus)*
  - Upload `.txt` files or paste tour text
  - Ask questions through a web interface
  - Displays grounded answers or web search fallback

---

## 🛠️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```
### 2. Ingest a Document
#### Text input
```bash
python main.py --ingest "Lady Gaga will tour Berlin and LA in 2025."
```
#### Or from file
```bash
python main.py --ingest path/to/your_file.txt
```
### ❓ 3. Ask a Question
```bash
python main.py --ask "Where will Lady Gaga perform in 2025?"
```
#### If the answer is not found locally, you'll see a fallback like:
❌ No relevant documents found locally. Searching online...

🌍 Online Search Results:
- Lady Gaga Announces 2025 Tour Dates
- ...
### 4. Run the Streamlit
```bash
streamlit run app/ui_streamlit.py
```



### Project Structure
├── app/<br>
│   ├── ingestion.py<br>
│   ├── qa.py<br>
│   ├── online_search.py<br>
│   └── ui_streamlit.py<br>
├── data/<br>
├── main.py<br>
├── README.md<br>
└──requirements.txt<br>


### 🧠 Models Used

| Purpose        | Model                          |
|----------------|--------------------------------|
| Summarization  | `sshleifer/distilbart-cnn-12-6` |
| Embedding      | `all-MiniLM-L6-v2`              |
| QA Generation  | `google/flan-t5-small`          |


<br>
<br>
👤 Author<br>
Sargis Grigoryan<br>
GitHub: GrigoryanSargis<br>
