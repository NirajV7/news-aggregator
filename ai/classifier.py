from transformers import pipeline
import requests
import os
from dotenv import load_dotenv
import time

#Load environment variables
load_dotenv()
NEWS_API_KEY =os.getenv('NEWS_API_KEY')

def fetch_news(api_key, catergory="technology", country="us", page_size=5):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey" : api_key,
        "catergory": catergory,
        "country": country,
        "page_size": page_size
    }
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        data = response.json()
        return [article["title"] for article in data["articles"]]
    except Exception as e:
        print(f"Error Fetching news: {e}")
        return[]
    
def classify_news(headline):
    #Initialize classifier ( will download model for first time)'
    classifier = pipeline("zero-shot-classification",
                          model="facebook/bart-large-mnli")
    
    #Define new categories
    candidate_labels = [
        "Technology" , "Business" , "Politics",
        "Sports" , "Entertainment" , "Science" ,
        "Health" , "Environment", "Education"
    ]
    
    #Classify the headline
    result = classifier(headline, candidate_labels)
    
    #Get Top Results
    top_topic = result['labels'][0]
    confidence = result['scores'][0]
    
    return top_topic, confidence

#Test Function
def main():
    if not NEWS_API_KEY:
        print("Error: NEWSAPI key is not found")
        return
    
    print("Fetching latest news headlines...")
    headlines = fetch_news(NEWS_API_KEY,catergory="technology")
    
    if not headlines:
        print("No headlines found. Check your API key or different category")
        return
    
    print(" AI News Classifier Initializing")
    print("(First run may take 1-2 minutes to download the model)")
    print("-" * 50 )
    
    for headline in headlines:
        start_time = time.time()
        topic, confidence = classify_news(headline)
        elapsed=time.time() - start_time
        
        print(f"Headline: {headline}")
        print(f"Topic: {topic} ({confidence:.0%} confidence)")
        print(f"Processing Time: {elapsed:.2f} seconds")
        print("-" *50)
        
if __name__ == "__main__":
    main()