# ⚡ Real-Time News Intelligence Pipeline (RAG Architecture)

> An automated Retrieval-Augmented Generation (RAG) system delivering hallucination-free, source-grounded news intelligence indexed via Pinecone Vector Database and synthesized with Google Gemini.

[![Live Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://realtime-news-rag.streamlit.app)

---

## 🎯 Problem Statement
Standard LLMs suffer from knowledge cutoffs and severe hallucinations when asked about fast-moving real-time global news and industry movements. This project builds an automated, verifiable pipeline that continuously indexes structured news feeds into high-dimensional vector spaces and enforces strictly grounded synthesis with evidence citations.

---

## 🏗️ Architecture & Pipeline Flow

```text
[ Google News RSS Feeds / Live Scraping ]
                 │
                 ▼
       [ Sentence Transformers ] ──▶ Dense Embeddings (all-MiniLM-L6-v2)
                 │
                 ▼
   [ Pinecone Vector Index ] ──▶ Cosine Similarity Storage
                 │
   [ User Query via Streamlit ] ──▶ Real-time Vector Search (Top-k Retrieval)
                 │
                 ▼
   [ Strict Prompt Grounding ] ──▶ Zero Hallucination Enforced
                 │
                 ▼
    [ Google Gemini Engine ] ──▶ Contextual Answer + Source Attribution