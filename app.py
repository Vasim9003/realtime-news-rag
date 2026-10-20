import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Setup
pc = Pinecone(api_key="pcsk_5ctgLG_BS2s3B5TUmrExjq6MsbiQkUokQek3U7huDCj5iwFVyqsVBgKPr3Sd47Rut1Wg1P")
index = pc.Index("news-index")
model = SentenceTransformer('all-MiniLM-L6-v2')

def fetch_google_news():
    # Google News India RSS Feed (English)
    url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    articles = soup.find_all('item')

    print(f"Fetched {len(articles)} articles from Google News!")

    for i, article in enumerate(articles[:20]): # Top 20 news mattum
        title = article.title.text
        link = article.link.text
        pub_date = article.pubDate.text

        # Vector conversion
        vector = model.encode(title).tolist()

        # Pinecone upload (ID-ah unique-ah vekkalam using timestamp)
        index.upsert(vectors=[{
            "id": f"gn_news_{i}",
            "values": vector,
            "metadata": {"title": title, "url": link, "date": pub_date, "source": "Google News"}
        }])

    print("✅ Google News uploaded to Pinecone!")

if __name__ == "__main__":
    fetch_google_news()