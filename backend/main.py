import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel , Field #For request data validation
from dotenv import load_dotenv #For environment variables
from typing import List #For type hints
import requests #For NewsAPI calls
import logging

#Load Environment Variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

#Import for our custom Ai Functions
from ai.classifier import classify_news

#FastAPI Setup
app = FastAPI(
    title="News Classifier API",
    description="API for classifying news headlines into topics",
    version="1.0.0"
)

#CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #In production , replace with frontend url
    allow_methods=["*"], #Allow all HTTP methods
    allow_headers=["*"], #Allow all headers
)
    
class NewsQuery(BaseModel):
    category: str = "technology" 
    country: str = "us"
    page_size: int = Field(5, ge=1, le=20)  # Validate 1-20 items
    
def fetch_news(api_key: str, category: str, country: str, page_size: int) -> List[dict]:
    """Fetch news headlines from NewsAPI with error handling"""
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "category": category,  # Fixed typo from 'catergory'
        "country": country,
        "pageSize": page_size  # NewsAPI expects camelCase
    }
    
    try:
        logger.info(f"Fetching {page_size} {category} headlines")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return [
            {
                "headline": article["title"],
                "url": article["url"],
                "source": article["source"]["name"]
            }
            for article in response.json().get("articles", [])
            if article.get("title") and article.get("url")  # Validate required fields
        ]
    except Exception as e:
        logger.error(f"NewsAPI Error: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch news: {str(e)}"
        )

#API Endpoints
@app.post("/news")
async def get_news(query: NewsQuery):
    try:
        logger.info(f"Fetching news with parms: {query}")
        
        #Verify API key is loaded
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            logger.error("NEWS_API_KEY not found in environment variables")
            
        # # Fetch raw news
        articles = fetch_news(
            api_key = api_key,
            category=query.category,
            country=query.country,
            page_size=query.page_size
        )
        
        logger.info(f"Fetched {len(articles)} headlines")
        
         # Process and classify
        results = []
        for article in articles:
            try:
                topic, confidence = classify_news(article["headline"])
                results.append({
                    **article,  # Include all original fields
                    "topic": topic,
                    "confidence": f"{confidence:.0%}",
                    "success": True
                })
            except Exception as e:
                logger.warning(f"Classification failed for '{article['headline'][:50]}...'")
                results.append({
                    **article,
                    "topic": "Classification Error",
                    "confidence": "0%",
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "meta": {
                "count": len(results),
                "successful": sum(1 for r in results if r["success"]),
                "category": query.category
            },
            "results": results
        }
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"News processing failed: {str(e)}"
        )

        
#Server StartUp
if __name__ == "__main__":
    import uvicorn
    
    # Start the FastAPI server
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,       # Default port for FastAPI 
        reload=True      # Auto-reload during development
    )