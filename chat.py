import google.generativeai as genai
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# 1. Setup API Keys (Direct-ah paste panniyachu)
PINECONE_KEY = "pcsk_5ctgLG_BS2s3B5TUmrExjq6MsbiQkUokQek3U7huDCj5iwFVyqsVBgKPr3Sd47Rut1Wg1P"
GEMINI_KEY = "AIzaSyDiPVi7_OMLuHD-Csg7YcsH9Zd_GSHTyeA"

# 2. Pinecone Initialize
pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index("news-index")

# 3. Gemini Initialize (IMPORTANT: Key correct-ah pass aaganum)
genai.configure(api_key=GEMINI_KEY)
llm = genai.GenerativeModel('gemini-2.5-flash')

# 4. Embedding Model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_answer(user_query):
    print(f"\n🔍 Searching for: {user_query}...")
    
    # A. Text-ah Vector-ah mathuroom
    query_vector = embed_model.encode(user_query).tolist()

    # B. Pinecone search
    results = index.query(vector=query_vector, top_k=2, include_metadata=True)

    # C. Context prepare panroom
    context = ""
    for match in results['matches']:
        title = match['metadata']['title']
        link = match['metadata']['url']
        context += f"\nTitle: {title}\nLink: {link}\n"

    # News kidaikala na general answer kekurom
    if not context:
        prompt = f"The user is asking: {user_query}. I don't have news about this. Answer generally."
    else:
        prompt = f"Context: {context}\n\nUser Question: {user_query}\n\nAnswer based on news:"

    # D. Gemini Answer
    try:
        response = llm.generate_content(prompt)
        print("\n🤖 AI Answer:", response.text)
    except Exception as e:
        print(f"\n❌ Error with Gemini: {e}")

if __name__ == "__main__":
    query = input("Ask me anything about tech news: ")
    get_answer(query)