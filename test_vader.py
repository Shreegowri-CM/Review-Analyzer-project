from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
print("good quality:", analyzer.polarity_scores("good quality"))
print("The battery is good, but the screen is bad:", analyzer.polarity_scores("The battery is good, but the screen is bad"))
