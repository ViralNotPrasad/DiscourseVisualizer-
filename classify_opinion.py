import paralleldots
paralleldots.set_api_key("p6OALWCwKka0MTpD1YyWRcDpJbYDo51kRwnEEIvPIUg")

def get_opinion(text):
    intent = paralleldots.intent(text)
    sentiment = paralleldots.sentiment(text)
    abuse = paralleldots.abuse(text)
    emotion = paralleldots.emotion(text)
    return intent,sentiment,abuse, emotion

def get_keywords(text):
    keywords = paralleldots.keywords(text)
    print (keywords)
