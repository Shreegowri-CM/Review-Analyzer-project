from transformers import pipeline
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

try:
    emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    try:
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    except KeyError:
        summarizer = None
except Exception as e:
    print(f"Error initializing pipelines: {e}")
    emotion_pipeline = None
    summarizer = None

async def analyze_sentiment(text: str):
    try:
        vs = analyzer.polarity_scores(text)
        compound = vs['compound']
        
        if compound >= 0.05:
            label = "POSITIVE"
            score = (compound + 1) / 2
        elif compound <= -0.05:
            label = "NEGATIVE"
            score = 1 - ((compound + 1) / 2)
        else:
            label = "NEUTRAL"
            score = 1 - abs(compound)
            
        return {"label": label, "score": float(score)}
    except Exception as e:
        print(f"Sentiment error: {e}")
        return {"label": "NEUTRAL", "score": 0.5}

async def detect_emotion(text: str):
    try:
        result = emotion_pipeline(text)[0]
        return {"emotion": result["label"], "score": result["score"]}
    except Exception as e:
        print(f"Emotion error: {e}")
        return {"emotion": "neutral", "score": 0.5}

async def analyze_aspects(text: str):
    aspects = [
        (re.compile(r"\b(battery|charge|power)\b", re.I), "Battery"),
        (re.compile(r"\b(screen|display|pixels)\b", re.I), "Screen"),
        (re.compile(r"\b(shipping|delivery|time)\b", re.I), "Shipping"),
        (re.compile(r"\b(price|cost|value)\b", re.I), "Price"),
        (re.compile(r"\b(sound|audio|bass)\b", re.I), "Audio"),
        (re.compile(r"\b(quality|build|material)\b", re.I), "Build Quality"),
    ]
    # Split text into sentences or clauses
    sentences = re.split(r'[.,;!]+|\s+but\s+|\s+and\s+', text, flags=re.IGNORECASE)
    found_aspects = []
    
    for sentence in sentences:
        if not sentence.strip(): continue
        
        words = sentence.split()
        if not words: continue
        
        aspect_matches = []
        for i, word in enumerate(words):
            for pattern, name in aspects:
                if pattern.search(word):
                    aspect_matches.append((i, name, word))
                    break
                    
        # Merge adjacent aspects of the same type
        merged = []
        for a in aspect_matches:
            if not merged or merged[-1][1] != a[1]:
                merged.append(a)
        aspect_matches = merged
                    
        for j, (idx, name, word) in enumerate(aspect_matches):
            left_bound = 0 if j == 0 else aspect_matches[j-1][0] + 1
            right_bound = len(words) if j == len(aspect_matches)-1 else aspect_matches[j+1][0]
            
            start_i = max(left_bound, idx - 4)
            end_i = min(right_bound, idx + 5)
            
            context = " ".join(words[start_i:end_i])
            
            vs = analyzer.polarity_scores(context)
            compound = vs['compound']
            
            if "on time" in context.lower():
                compound += 0.5
                
            if compound >= 0.05:
                sentiment = "POSITIVE"
            elif compound <= -0.05:
                sentiment = "NEGATIVE"
            else:
                sentiment = "NEUTRAL"
                
            found_aspects.append({
                "aspect": name,
                "sentiment": sentiment,
                "context": context
            })
            
    # Deduplicate keeping the first occurrence per aspect
    unique_aspects = {}
    for a in found_aspects:
        if a["aspect"] not in unique_aspects:
            unique_aspects[a["aspect"]] = a
            
    return list(unique_aspects.values())

async def detect_fake_review(text: str, rating: int):
    fake_score = 0.0
    reasons = []

    if len(text) < 10 and rating == 5:
        fake_score += 0.4
        reasons.append("Overly brief 5-star review.")
    
    if "http" in text or ".com" in text:
        fake_score += 0.9
        reasons.append("Contains links (spam).")
    
    uppercase_count = sum(1 for c in text if c.isupper())
    if uppercase_count > len(text) * 0.5:
        fake_score += 0.3
        reasons.append("High uppercase ratio.")
    
    is_fake = fake_score > 0.6
    return {
        "isFake": is_fake,
        "fakeScore": min(fake_score, 1.0),
        "reasons": reasons
    }

async def generate_summary(text: str):
    if len(text.split()) < 15:
        return text  # Too short to summarize
    if summarizer is None:
        return text[:100] + "..." if len(text) > 100 else text
    try:
        res = summarizer(text, max_length=min(40, max(10, int(len(text.split())*0.8))), min_length=5, do_sample=False)
        return res[0]['summary_text']
    except Exception as e:
        print(f"Summarizer error: {e}")
        return text

async def detect_tags_and_suggestions(text: str, aspects: list, sentiment: str):
    tags = []
    suggestions = []
    text_lower = text.lower()
    
    if "ship" in text_lower or "deliver" in text_lower or "arrive" in text_lower:
        tags.append("Shipping & Logistics")
    if "broke" in text_lower or "defect" in text_lower or "stop working" in text_lower:
        tags.append("Product Defect")
    if "cheap" in text_lower or "overpriced" in text_lower or "worth" in text_lower:
        tags.append("Pricing Feedback")
    if "love" in text_lower or "amazing" in text_lower or "perfect" in text_lower:
        tags.append("Highly Praised")
        
    if sentiment == "NEGATIVE":
        for a in aspects:
            aspect_name = a["aspect"]
            if aspect_name == "Battery":
                suggestions.append("Investigate battery life degradation or supplier quality.")
            elif aspect_name == "Build Quality":
                suggestions.append("Review manufacturing tolerances and material durability.")
            elif aspect_name == "Shipping":
                suggestions.append("Audit logistics partner for delayed deliveries.")
            elif aspect_name == "Price":
                suggestions.append("Evaluate price competitiveness versus market alternatives.")
    
    if len(tags) == 0:
        tags.append("General Feedback")
        
    return tags, list(set(suggestions))

async def run_ai_pipeline(text: str, rating: int, user_id: str = None):
    sentiment = await analyze_sentiment(text)
    emotion = await detect_emotion(text)
    fake_detection = await detect_fake_review(text, rating)
    aspects = await analyze_aspects(text)
    
    summary = await generate_summary(text)
    tags, suggestions = await detect_tags_and_suggestions(text, aspects, sentiment["label"])
    
    return {
        "sentiment": sentiment,
        "emotion": emotion,
        "aspects": aspects,
        "fakeDetection": fake_detection,
        "summary": summary,
        "tags": tags,
        "suggestions": suggestions
    }
