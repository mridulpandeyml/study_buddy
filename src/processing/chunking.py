import re

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of roughly `chunk_size` words with `overlap` words.
    Simple and fast token-like chunking.
    """
    if not text:
        return []
    
    # Clean text to normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split(' ')
    
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
            
    return chunks
