from app.ingestion import DocumentIngestor
from app.qa import QuestionAnsweringEngine
import argparse
import os
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


def run_ingest(input_text_or_path):
    ingestor = DocumentIngestor()

    if os.path.exists(input_text_or_path):
        with open(input_text_or_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = input_text_or_path

    result = ingestor.ingest(text)
    print(result)

def run_query(query):
    engine = QuestionAnsweringEngine()
    response = engine.answer(query)
    print("Answer:", response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concert Tour RAG Bot CLI")
    parser.add_argument("--ingest", type=str, help="Plain text OR path to file to ingest")
    parser.add_argument("--ask", type=str, help="Ask a question based on ingested documents")

    args = parser.parse_args()

    if args.ingest:
        run_ingest(args.ingest)
    elif args.ask:
        run_query(args.ask)
    else:
        print("Use --ingest <text_or_file> to ingest or --ask <question> to query.")
