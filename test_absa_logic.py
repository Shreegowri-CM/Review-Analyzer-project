import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_aspects(text: str):
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

print(analyze_aspects("battery is good quality is bad and delivery was on time"))
