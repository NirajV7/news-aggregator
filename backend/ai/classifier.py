from transformers import pipeline
import logging

#Configure logging
logger = logging.getLogger(__name__)

# Initialize classifier globally to avoid reloading
classifier = None

def initialize_classifier():
    """Lazy initialization of the classifier"""
    global classifier
    if classifier is None:
        logger.info("Initializing NLP classifier")
        classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=-1,
            torch_dtype="auto"
        )
    return classifier

def classify_news(headline):
    """
    Classify a news headline into predefined topics
    Args:
        headline (str): News headline text
    Returns:
        tuple: (topic, confidence_score)
    """
    if not headline or not isinstance(headline, str):
        logger.warning("Invalid headline received")
        return "General News", 0.0
    
    try:
        model = initialize_classifier()
        candidate_labels = [
            "Technology & Computing",
            "Business & Finance",
            "Politics & Government",
            "Sports & Athletics",
            "Entertainment & Celebrities",
            "Science & Research",
            "Health & Medicine",
            "Environment & Climate",
            "Education & Schools"
        ]
        
        result = model(headline, candidate_labels)
        topic = result['labels'][0]
        confidence = result['scores'][0]
        
        return topic, confidence
        
    except Exception as e:
        logger.error(f"Classification failed: {str(e)}")
        return "General News", 0.0
    

