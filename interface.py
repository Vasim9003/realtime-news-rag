import streamlit as st
import google.generativeai as genai
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os

# --- Setup Secrets (Streamlit Cloud & Local fallback) ---
PINECONE_KEY = st.secrets.get("PINECONE_API_KEY", os.getenv("PINECONE_API_KEY", "pcsk_5ctgLG_BS2s3B5TUmrExjq6MsbiQkUokQek3U7huDCj5iwFVyqsVBgKPr3Sd47Rut1Wg1P"))
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "AIzaSyDiPVi7_OMLuHD-Csg7YcsH9Zd_GSHTyeA"))

# --- Cache models so it doesn't reload on every click ---
@st.cache_resource
def load_resources():
    pc = Pinecone(api_key=PINECONE_KEY)
    index = pc.Index("news-index")
    genai.configure(api_key=GEMINI_KEY, transport="rest")
    llm = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    return index, llm, embed_model

index, llm, embed_model = load_resources()

# --- UI Layout ---
st.set_page_config(page_title="Tech News AI", page_icon="🤖")
st.title("🤖 Real-Time News Intelligence (RAG)")
st.markdown("Ask anything about tech news and layoffs indexed in Pinecone.")

query = st.text_input("Enter your question:", placeholder="e.g. Is there any news about Google or tech layoffs?")

if st.button("Ask AI"):
    if query:
        with st.spinner("Searching Pinecone database..."):
            query_vector = embed_model.encode(query).tolist()
            results = index.query(vector=query_vector, top_k=3, include_metadata=True)
            
            context = ""
            sources = []
            for match in results['matches']:
                title = match['metadata'].get('title', '')
                url = match['metadata'].get('url', '')
                context += f"\nTitle: {title}\nLink: {url}\n"
                if url:
                    sources.append(url)
            
            if not context.strip():
                st.warning("No relevant news records found in the index.")
            else:
                prompt = f"Context:\n{context}\n\nUser Question: {query}\n\nAnswer concisely based strictly on the context and cite facts:"
                response = llm.generate_content(prompt)
                
                st.subheader("AI Answer:")
                st.write(response.text)
                
                with st.expander("See Verified Sources (From Pinecone)"):
                    for s in set(sources):
                        st.markdown(f"- [{s}]({s})")
    else:
        st.warning("Please enter a question first!")