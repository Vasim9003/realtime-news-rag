import streamlit as st
import requests
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os

# --- Setup Secrets ---
PINECONE_KEY = st.secrets.get("PINECONE_API_KEY", os.getenv("PINECONE_API_KEY", "pcsk_5ctgLG_BS2s3B5TUmrExjq6MsbiQkUokQek3U7huDCj5iwFVyqsVBgKPr3Sd47Rut1Wg1P"))
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "AIzaSyDiPVi7_OMLuHD-Csg7YcsH9Zd_GSHTyeA"))

@st.cache_resource
def load_resources():
    pc = Pinecone(api_key=PINECONE_KEY)
    index = pc.Index("news-index")
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    return index, embed_model

index, embed_model = load_resources()

def call_gemini(prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error from Gemini API ({response.status_code}): {response.text}"

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
                ai_answer = call_gemini(prompt)
                
                st.subheader("AI Answer:")
                st.write(ai_answer)
                
                with st.expander("See Verified Sources (From Pinecone)"):
                    for s in set(sources):
                        st.markdown(f"- [{s}]({s})")
    else:
        st.warning("Please enter a question first!")