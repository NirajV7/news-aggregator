import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel #For request data validation
from dotenv import load_dotenv #For environment variables
from typing import List #For type hints
import requests #For NewsAPI calls
import logging

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

#Import for our custom Ai Functions
from ai.classifier import classify_news, fetch_news

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
#Data Models
class NewsItem(BaseModel):
    headline:str #The news headline to classify
    
class NewsQuery(BaseModel):
    category: str = "technology" 
    country: str = "us"
    page_size: int = 5
    
#API Endpoints
@app.post("/classify")
async def classify(item: NewsItem):
    try:
        #Call AI classification function
        topic, confidence = classify_news(item.headline)
        
        return{
            "topic":topic,
            "confidence":f"{confidence:.0%}", #converts to percentage
            "headline": item.headline
        }
    except Exception as e:
        #Handle errors 
        raise HTTPException(
            status_code=500,
            detail=f"Classifcation failed : {str(e)}"
        )
        
@app.post("/fetch-and-classify")
async def fetch_and_classify(query:NewsQuery):
    try:
        
        logger.info(f"Fetching news with parms: {query}")
        
        #Verify API key is loaded
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            logger.error("NEWS_API_KEY not found in environment variables")
            
        #fetch headlines from news api
        headlines=fetch_news(
            api_key,
            catergory=query.category,
            country=query.country,
            page_size=query.page_size
        )
        
        logger.info(f"Fetched {len(headlines)} headlines")
        
        # 2. Process headlines with error handling
        results = []
        for i, headline in enumerate(headlines):
            try:
                # Clean headline
                clean_headline = headline.strip()[:500]  # Limit length
                
                # Classify
                topic, confidence = classify_news(clean_headline)
                
                results.append({
                    "headline": headline,
                    "topic": topic,
                    "confidence": f"{confidence:.0%}",
                    "success": True
                })
                
                logger.info(f"Processed {i+1}/{len(headlines)}: {topic}")
                
            except Exception as e:
                logger.warning(f"Failed to classify '{headline[:50]}...': {str(e)}")
                results.append({
                    "headline": headline,
                    "topic": "Error",
                    "confidence": "0%",
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "count": len(results),
            "successful": sum(1 for r in results if r["success"]),
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"News fetching failed: {str(e)}"
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