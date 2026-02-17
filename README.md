# Personal PDF RAG Chatbot 🚀

**Chat with your PDFs. Get instant answers with citations.**

A fast, local-first Retrieval-Augmented Generation (RAG) chatbot that lets you ask questions about your own PDFs—research papers, notes, books, reports, and more. 

Powered by **LlamaIndex**, **Chroma** vector DB, **Groq** for ultra-fast inference, and **Streamlit** for a beautiful web interface.

---

## ✨ Features

- 📄 **PDF Processing** – Automatically ingests and chunks PDFs
- 🔍 **Semantic Search** – Finds relevant document chunks instantly
- 💬 **Conversational Chat** – Chat history and context-aware responses
- 📑 **Accurate Citations** – Shows source file, page number, and relevance score
- ⚡ **Ultra-Fast** – Powered by Groq (Llama-3.3-70B)
- 💾 **Persistent Storage** – ChromaDB saves your index permanently
- 🆓 **Local First** – No cloud lock-in, run entirely on your machine
- 🎨 **Clean UI** – Professional Streamlit interface

---

## 🛠️ Tech Stack

| Component | Tool | Why |
|-----------|------|-----|
| **Framework** | LlamaIndex | Clean document → embed → query pipeline |
| **Vector DB** | ChromaDB | Fast, simple, fully local |
| **Embeddings** | nomic-ai/nomic-embed-text-v1.5 | Strong open-source performance |
| **LLM** | Groq (Llama-3.3-70B) | Lightning-fast inference |
| **UI** | Streamlit | Interactive chat in 100 lines |
| **PDF Parsing** | PyPDF | Reliable text extraction |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Groq API key** ([get free here](https://console.groq.com/keys))

### 1️⃣ Clone & Install

```bash
git clone https://github.com/ishpatel21/pdf-rag-chatbot.git
cd pdf-rag-chatbot
pip install -r requirements.txt
```

### 2️⃣ Setup API Key

Create a `.env` file in the root directory:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Or set it as an environment variable:

```bash
export GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3️⃣ Add Your PDFs

Place PDF files in the `./data` folder:

```
data/
├── paper1.pdf
├── paper2.pdf
└── notes.pdf
```

### 4️⃣ Index Your PDFs (First Time Only)

Run this once to create the vector index:

```bash
python3 index_pdfs.py
```

**What it does:**
- ✅ Reads all PDFs from `./data`
- ✅ Chunks and embeds them
- ✅ Saves to persistent `./chroma_db`

**Time:** ~1-5 minutes depending on PDF size

### 5️⃣ Launch the Chat Interface

```bash
streamlit run app_streamlit.py
```

Opens automatically at `http://localhost:8501` (or `8502` if port is busy)

---

## 💬 Usage Examples

Once the app is running, try asking:

- *"Summarize the main ideas"*
- *"What are the key findings?"*
- *"Explain this concept in simple terms"*
- *"Compare these two sections"*
- *"What was mentioned on page 5?"*

**Every answer includes citations:**
```
Answer: [LLM response here]

**Sources:**
- [1] filename.pdf (page 3, score 0.92)
  > "Relevant excerpt from the document..."
```

---

## 📁 Project Structure

```
pdf-rag-chatbot/
├── data/                 # ← Drop your PDFs here
├── chroma_db/            # ← Auto-created vector index (persistent)
├── app.py                # Original console interface
├── app_streamlit.py      # Streamlit web interface ⭐
├── index_pdfs.py         # Indexing script
├── requirements.txt      # Dependencies
├── .env.example          # Example environment file
└── README.md             # This file
```

---

## 🔄 Workflow

### First Time
```bash
python3 index_pdfs.py      # Build the index
streamlit run app_streamlit.py  # Start chatting
```

### Adding New PDFs
```bash
# 1. Drop new PDFs in ./data folder
# 2. Re-run indexing (deletes old, creates new)
python3 index_pdfs.py

# 3. Restart the app
streamlit run app_streamlit.py
```

### Just Chatting (No Changes)
```bash
streamlit run app_streamlit.py  # Uses existing index
```

---

## 🎯 Future Enhancements

- [ ] File uploader in Streamlit sidebar
- [ ] Re-index button without restarting
- [ ] Streaming responses
- [ ] Hybrid search (keyword + semantic)
- [ ] Custom chunk size/overlap settings
- [ ] Deploy to Streamlit Cloud
- [ ] Fallback to OpenAI/Ollama

---

## 📊 Performance

| Task | Time |
|------|------|
| Index 15-page PDF | ~2 min |
| Average query response | ~1-2 sec |
| Browser load time | <1 sec |

---

## 🔒 Privacy & Storage

- ✅ **All local** – No data sent to external servers
- ✅ **Persistent** – Index saved in `./chroma_db`
- ✅ **No cloud lock-in** – Own your data completely
- ✅ **API key** – Only Groq API key sent externally for LLM inference

---

## ⚠️ Troubleshooting

### "Collection pdf_rag does not exist"
**Solution:** Run `python3 index_pdfs.py` first

### "GROQ_API_KEY not found"
**Solution:** Add `.env` file with `GROQ_API_KEY=your_key`

### Slow indexing on large PDFs
**Normal:** Large PDFs take time to embed. Grab coffee ☕

### Out of memory
**Solution:** Process smaller PDFs or increase chunk overlap in `index_pdfs.py`

---

## 📝 License

MIT License – Feel free to fork, modify, and use in your own projects!

---

## 🤝 Contributing

Pull requests welcome! Ideas:
- Better PDF parsing
- Alternative embedding models
- UI improvements
- Performance optimizations

---

## 📧 Questions?

Open an issue on GitHub or check the [LlamaIndex docs](https://docs.llamaindex.ai).

---

**Built with ❤️ for local AI & knowledge management**
