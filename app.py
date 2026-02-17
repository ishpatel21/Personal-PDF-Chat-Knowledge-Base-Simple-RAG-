import os
import ssl
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb

# Fix SSL certificate verification issues for NLTK downloads
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()

# ================= CONFIG =================
PDF_FOLDER = "data"                  # change if needed
CHROMA_PATH = "./chroma_db"          # persistent folder
COLLECTION_NAME = "pdf_rag"          # collection name in Chroma
EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"   # good & fast (~137M params)
GROQ_MODEL = "llama-3.3-70b-versatile"           # or "llama3-70b-8192" or "mixtral-8x7b-32768"
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 200
# ==========================================

# Global settings (affects all indices)
Settings.embed_model = HuggingFaceEmbedding(
    model_name=EMBED_MODEL,
    trust_remote_code=True
)
Settings.llm = Groq(model=GROQ_MODEL, temperature=0.1)

def build_or_load_index():
    # Initialize Chroma client & collection (persistent)
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # If index already exists → load it
    if chroma_collection.count() > 0:
        print(f"Loading existing index from {CHROMA_PATH} ({chroma_collection.count()} vectors)...")
        index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    else:
        print("Building new index...")
        # Load PDFs
        documents = SimpleDirectoryReader(
            PDF_FOLDER,
            required_exts=[".pdf"],
        ).load_data()

        if not documents:
            raise ValueError(f"No PDFs found in {PDF_FOLDER}")

        print(f"Loaded {len(documents)} documents.")

        # Build index (chunk + embed + store)
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True,
        )
        # Persist (already done via Chroma PersistentClient, but explicit call for safety)
        index.storage_context.persist(persist_dir=CHROMA_PATH)
        print("Index built and persisted.")

    return index


def main():
    index = build_or_load_index()
    query_engine = index.as_query_engine(
        similarity_top_k=4,          # retrieve top 4 chunks
        response_mode="compact",     # or "tree_summarize" if you want more compression
    )

    print("\n" + "="*60)
    print("PDF RAG Chat (Day 1 version) – type 'exit' to quit")
    print("Upload PDFs to 'data/' folder and re-run to add them.")
    print("="*60 + "\n")

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        if not question:
            continue

        try:
            response = query_engine.query(question)

            print("\nAnswer:")
            print(response.response.strip())

            print("\nSources:")
            for i, node in enumerate(response.source_nodes, 1):
                score = node.score if node.score else "?"
                text = node.text.strip()[:220] + "..." if len(node.text) > 220 else node.text.strip()
                file_name = node.metadata.get("file_name", "unknown")
                page = node.metadata.get("page_label", "?")
                print(f"  [{i}]  {file_name}  (page {page})  score={score:.3f}")
                print(f"      {text}\n")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()