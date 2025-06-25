import csv
from newspaper import Article
from pathlib import Path
from typing import List, Dict

def fetch_article_text(url: str) -> Dict[str, str]:
    article = Article(url)
    try:
        article.download()
        article.parse()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return {"url": url, "title": "", "authors": "", "publish_date": "", "text": ""}
    
    return {
        "url": url,
        "title": article.title,
        "authors": ", ".join(article.authors),
        "publish_date": article.publish_date.isoformat() if article.publish_date else "",
        "text": article.text.replace("\n", " ")
    }

def fetch_articles(urls: List[str]) -> List[Dict[str, str]]:
    articles = []
    for u in urls:
        print(f"→ Fetching {u}")
        meta = fetch_article_text(u)
        articles.append(meta)
    return articles

def save_articles_csv(articles: List[Dict[str, str]], out_path: Path):
    fieldnames = ["url", "title", "authors", "publish_date", "text"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for art in articles:
            writer.writerow(art)
    print(f"Saved {len(articles)} articles to {out_path}")

if __name__ == "__main__":
    urls = [
        "https://www.espn.com.au/nba/story/_/id/45570730/nba-playoff-mvps-which-thunder-pacers-join-sga-top-5"
        
    ]
    arts = fetch_articles(urls)
    save_articles_csv(arts, Path("data/articles/articles.csv"))
