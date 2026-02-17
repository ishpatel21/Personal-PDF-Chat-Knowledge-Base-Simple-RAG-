import streamlit as st
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

# Config same as before
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "pdf_rag"
Settings.embed_model = HuggingFaceEmbedding(model_name="nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
Settings.llm = Groq(model="llama-3.3-70b-versatile", temperature=0.1)

# Load index
@st.cache_resource
def load_index():
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = chroma_client.get_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    return VectorStoreIndex.from_vector_store(vector_store)

index = load_index()
query_engine = index.as_query_engine(similarity_top_k=4)

# Streamlit UI
st.title("Personal PDF Knowledge Base – RAG Chat")
st.markdown("Ask questions about your PDFs. Answers include citations.")

# Chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_engine.query(prompt)

            answer = response.response
            sources = "\n\n**Sources:**\n"
            for i, node in enumerate(response.source_nodes, 1):
                file_name = node.metadata.get("file_name", "unknown")
                page = node.metadata.get("page_label", "?")
                score = node.score or "?"
                text = node.text.strip()[:200] + "..." if len(node.text) > 200 else node.text.strip()
                sources += f"- **[{i}] {file_name}** (page {page}, score {score:.2f})\n  > {text}\n"

            full_response = answer + sources
            st.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
