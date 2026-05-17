import spacy
from collections import Counter

nlp = None

def get_nlp():
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spacy en_core_web_sm model...")
            from spacy.cli import download
            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
    return nlp

def extract_topics_and_keywords(text):
    """Extracts main topics and keywords from the text using NLP."""
    if not text:
        return {"topics": [], "keywords": []}
        
    doc = get_nlp()(text)
    
    # Extract entities as topics (simplified)
    entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'PERSON', 'EVENT', 'LAW', 'WORK_OF_ART']]
    topic_counts = Counter(entities)
    top_topics = [topic for topic, count in topic_counts.most_common(5)]
    
    # Extract keywords (nouns, proper nouns, adjectives)
    keywords = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'PROPN', 'ADJ']]
    keyword_counts = Counter(keywords)
    top_keywords = [kw for kw, count in keyword_counts.most_common(10)]
    
    return {
        "topics": list(set(top_topics)),
        "keywords": top_keywords
    }

def analyze_difficulty(text):
    """Simple heuristic to estimate text difficulty."""
    if not text:
        return "Beginner"
        
    doc = get_nlp()(text)
    sentences = list(doc.sents)
    if len(sentences) == 0:
         return "Beginner"
         
    avg_sentence_length = len(doc) / len(sentences)
    
    if avg_sentence_length > 25:
        return "Advanced"
    elif avg_sentence_length > 15:
        return "Standard"
    else:
        return "Beginner"
