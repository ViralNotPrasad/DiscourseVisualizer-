import pickle
import nltk
from nltk.tokenize import word_tokenize
import classify_opinion
import sys
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('wordnet')
nltk.download('stopwords')

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

en_stop = set(nltk.corpus.stopwords.words('english'))

# for each opinion, find out which topic it is about, and whether it is pro or anti


def main():

    with open("data_1-15-43.pickle", "rb") as data:
        d = pickle.load(data)

    ids = d["id"]
    titles = d["title"]
    titles = [elem.strip("CMV:").strip() for elem in titles]
    bodies = d["body"]
    scores = d["score"]
    comments = d["comments"]
    comms_num = d["comms_num"]
    created = d["created"]
    # print (classify_opinion.get_keywords(bodies[:5]))
    topics = {"abortion":[], "immigration":[], "shooting":[], "android":[],"education":[],"other":[]}
    # topics_pro = {"abortion":[], "immigration":[], "shooting":[], "android":[],"other":[]}
    # topics_anti = {"abortion":[], "immigration":[], "shooting":[], "android":[],"other":[]}
    process_bodies(bodies)
    titles_tok = tokenize(titles)
    bodies_tok = tokenize(bodies)
    corpus = [titles_tok[i] for i in range(len(titles_tok))]

    immigration = ["immigration", "immigrant", "refugee", "mexican", "border", "immigrants"]
    shooting = ["gunman", "shooting", "gun", "armed", "firearm", "shootings"]
    abortion = ["baby", "fetus", "abort", "abortion", "trimester", "pregnant", "pregnancy"]
    android = ["android","ios","phone","smartphone","apple"]
    education = ["university", "college", "student", "debt", "loan", "education"]
    # queries = expand_queries(immigration) # function to see which keywords to manually add to the list

    vectorizer_immi = TfidfVectorizer(vocabulary=immigration, ngram_range=(1,1))
    vectorizer_shoot = TfidfVectorizer(vocabulary=shooting, ngram_range=(1,1))
    vectorizer_abort = TfidfVectorizer(vocabulary=abortion, ngram_range=(1,1))
    vectorizer_android = TfidfVectorizer(vocabulary=android, ngram_range=(1,1))
    vectorizer_education = TfidfVectorizer(vocabulary=education, ngram_range=(1,1))

    matrix_dict = {"abortion":None, "immigration":None ,"shooting":None, "android":None,"education":None,"other":None}
    vectorizer_dict = {"immigration": vectorizer_immi, "abortion": vectorizer_abort, "shooting": vectorizer_shoot, "android": vectorizer_android, "education":vectorizer_education}
    # comment out next line to run for all topics
    # vectorizer_dict = {"education":vectorizer_education}

    for key in vectorizer_dict:
        matrix_dict[key] = vectorizer_dict[key].fit_transform(corpus).toarray()

    for i in range(len(bodies_tok)):
        max = -1
        category = "other"
        for key in vectorizer_dict:
            score = sum(matrix_dict[key][i])
            if score > max:
                max = score
                category = key
        if max == 0:
            category = "other"

        topics[category].append((i, score))

    for key in vectorizer_dict:
        topics[key].sort(key=lambda x : x[1], reverse=True)
        topics[key] = [elem[0] for elem in topics[key]]

    # for i in topics["shooting"]:
    #     print(titles[i])
    # print("---------------")
    # for i in topics["education"]:
    #     print(titles[i])

    finaldict = {"ids" : ids, "titles":titles, "bodies":bodies , "scores":scores, "comments":comments, "topics":topics, "comms_num":comms_num, "created":created}
    with open("finaldict.pickle", "wb") as f:
        pickle.dump(finaldict, f)
    return

def expand_queries(queries):
    for query in queries:
        for word in query.split(" "):
            print(find_synonyms(word))

def find_synonyms(word):
    synonyms = []
    for syn in wn.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())

    return synonyms

# experiments with sentiment analysis
def find_sentiment(text):
    return classify_opinion.get_opinion(text)


def print_polarity(topic, topics, titles, bodies, topics_pro, topics_anti):

    for i in topics[topic]:
        # print ("View:", bodies[i])
        # print("Opposite View:", comments[i][0])
        pol = find_sentiment(titles[i]+bodies[i])
        if pol["sentiment"] == "positive":
            topics_pro[topic].append(i)
            print("pro:",titles[i],bodies[i])
        elif pol["sentiment"] == "negative":
            topics_anti[topic].append(i)
            print("anti:",titles[i],bodies[i])


def process_bodies(bodies):
    for i in range(len(bodies)):
        temp = ["" if "happy cmving" in sent.casefold() else sent for sent in bodies[i].split("\n")]  # takes care of mod posts
        bodies[i] = "\n".join(temp)
    return

def tokenize(text):
    text_tok = []
    for l in text:
        temp = ["URL" if "www" in elem or "http" in elem or ".com" in elem or ".net" in elem or ".gov" in elem else elem.lower() for elem in word_tokenize(l)]
        temp = temp[2:] # remove 'cmv :' which appears at the start of each title
        text_tok.append(" ".join([get_lemma(elem) for elem in temp if elem not in en_stop and elem.isalnum()]))

    return text_tok

#binary categorization
def categorize_data(l):
    immigration = set(["immigration", "deport", "undocumented", "immigrant", "alien", "refugee"])
    shooting = set(["gunman", "shooting", "shot", "gun", "armed", "violence", "shoot", "firearm"])
    abortion = set(["baby", "fetus", "abort", "abortion", "trimester", "pregnant", "pregnancy"])
    android = set(["android","ios","phone","smartphone","apple" ,"touchscreen", "google"])
    dict = {"immigration" : 0,
    "shooting" : 0,
    "abortion" : 0,
    "android" : 0}


    THRESHOLD = 2
    count = 0
    for word in l:
        if word in immigration:
           dict["immigration"]+=1
           count+=1
        elif word in shooting:
            dict["shooting"]+=1
            count+=1
        elif word in abortion:
            dict["abortion"]+=1
            count+=1
        elif word in android:
            dict["android"]+=1
            count+=1

    if count <= THRESHOLD:
        return "other"
    l = [(k,dict[k]) for k in dict.keys()]
    return sorted(l, key=lambda x:x[1])[-1][0]


def print_dict(d):

    ids = d["id"]
    titles = d["title"]
    bodies = d["body"]
    scores = d["score"]
    comments = d["comments"]

    for i in range(len(ids)):
        print(ids[i])
        print(titles[i])
        print(bodies[i])
        print(scores[i])
        print(comments[i])
        print("\n")

    return

#lemmatization code
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma



if __name__ == '__main__':
    main()




# TODO: improve tokenization, use word2vec to find related words to a topic, use better sentiment analysis to categorize opinions
# TODO: expand list of topics - incarceration, drugs, apple vs android, etc.
# TODO: topic modelling for the topics of a viewpoint for visualization
# ideas - wordnet for similar words, to cluster, tf-idf or BM25 for finding relevant docs to "query"
