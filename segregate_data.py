import pickle
import nltk
from nltk.tokenize import word_tokenize

nltk.download('wordnet')
nltk.download('stopwords')

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

en_stop = set(nltk.corpus.stopwords.words('english'))

# for each opinion, find out which topic it is about, and whether it is pro or anti


def main():

    with open("data.pickle", "rb") as data:
        d = pickle.load(data)


    ids = d["id"]
    titles = d["title"]
    titles = [elem.strip("CMV:").strip() for elem in titles]
    bodies = d["body"]
    scores = d["score"]
    comments = d["comments"]

    political = {"abortion":[], "immigration":[], "shooting":[], "other":[]}

    process_bodies(bodies)
    titles_tok = tokenize(titles)

    for i in range(len(titles_tok)):
        category = categorize_data(titles_tok[i])
        political[category].append(i)

    for i in political["immigration"]:
        print ("View:", bodies[i])
        print("Opposite View:", comments[i][0])
    return


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
        text_tok.append([get_lemma(elem) for elem in temp if elem not in en_stop and elem.isalnum()])

    return text_tok


def categorize_data(l):
    immigration = set(["immigration", "illegal", "deport", "undocumented", "immigrant", "alien", "refugee"])
    shooting = set(["gunman", "shooting", "violence", "shot", "gun", "armed", "violence", "death", "control", "shoot", "mass", "firing"])
    abortion = set(["life", "choice", "baby", "fetus", "abort", "abortion", "trimester", "unwanted", "terminate", "pregnant", "pregnancy"])

    dict = {"immigration" : 0,
    "shooting" : 0,
    "abortion" : 0}

    THRESHOLD = 0
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


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


def find_related_words(word):
    pass


if __name__ == '__main__':
    main()




# TODO: improve tokenization, use word2vec to find related words to a topic, use better sentiment analysis to categorize opinions
# TODO: expand list of topics - incarceration, drugs, apple vs android, etc.
# TODO: topic modelling for the topics of a viewpoint for visualization
# ideas - wordnet for similar words, to cluster, tf-idf or BM25 for finding relevant docs to "query"
