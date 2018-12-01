import paralleldots
paralleldots.set_api_key("p6OALWCwKka0MTpD1YyWRcDpJbYDo51kRwnEEIvPIUg")

def get_opinion(text):
    return paralleldots.custom_classifier

def get_keywords(text):
    keywords = paralleldots.keywords(text)
    print (keywords)
