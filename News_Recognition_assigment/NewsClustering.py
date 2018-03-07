import re, pprint, os, numpy
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.metrics.cluster import *
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.cluster import adjusted_rand_score
from nltk.corpus import wordnet
import string


def filter_stopwords(token_list):
    stop = set(stopwords.words('english'))
    clean_tokens = []
    for token in token_list:
        if token[0] not in stop:
            clean_tokens.append(token)
    return clean_tokens

def wordnet_value(value):
    if value.startswith('J'):
        return wordnet.ADJ
    elif value.startswith('V'):
        return wordnet.VERB
    elif value.startswith('N'):
        return wordnet.NOUN
    elif value.startswith('R'):
        return wordnet.ADV
    else:
        return None

def lemmatize(token_list):
    lemmatizer = WordNetLemmatizer()
    result = []
    for token in token_list:
        if len(token) > 0:
            pos = wordnet_value(token[1])
            if pos !=None:
                lemma = lemmatizer.lemmatize(str(token[0]).lower(), pos=pos)
                result.append(lemma)
    return result

def remove_punctuation(token_list):
    result = []
    for token in token_list:
        if len(token)>0:
            punct_removed = ''.join([letter for letter in token if letter in string.ascii_letters])
            if punct_removed != '':
                result.append(punct_removed)
    return result

def process_text(text):
    tokens = nltk.word_tokenize(text)
    tokens_tags = nltk.pos_tag(tokens)
    tokens_lemmatize = lemmatize(tokens_tags)
    tokens_filter_stop_words = filter_stopwords(tokens)
    tokens_clean = remove_punctuation(tokens_filter_stop_words)
    return tokens_clean

def cluster_texts(texts, clustersNumber, distance):
    #Load the list of texts into a TextCollection object.
    collection = nltk.TextCollection(texts)
    print("Created a collection of {0}, terms.".format(len(collection)))

    #get a list of unique terms
    unique_terms = list(set(collection))
    print("Unique terms found: ", len(unique_terms))

    ### And here we actually call the function and create our array of vectors.
    vectors = [numpy.array(TF(f,unique_terms, collection)) for f in texts]
    print("Vectors created.")

    # initialize the clusterer
    clusterer = AgglomerativeClustering(n_clusters=clustersNumber,
                                      linkage="average", affinity=distance)
    clusters = clusterer.fit_predict(vectors)

    return clusters

# Function to create a TF vector for one document. For each of
# our unique words, we have a feature which is the tf for that word
# in the current document
def TF(document, unique_terms, collection):
    word_tf = []
    for word in unique_terms:
        word_tf.append(collection.tf(word, document))
    return word_tf

def main():
    folder = "/Txt/"
    abs_path=os.path.dirname(os.path.realpath(__file__))+folder
    # Empty list to hold text documents.
    texts = []
    listing = os.listdir(abs_path)
    for file in listing:
        # print("File: ",file)
        if file.endswith(".txt"):
            url = abs_path+file
            f = open(url, encoding="utf-8" ,errors='ignore')
            raw = f.read()
            f.close()
            texts.append(process_text(raw))
    print(texts)

    print("Prepared {0},  documents...".format(len(texts)))
    print("They can be accessed using texts[0] - texts[ {0}".format(str(len(texts) - 1)))
#
    distanceFunction = "cosine"
    # distanceFunction = "euclidean"
    test = cluster_texts(texts, 5, distanceFunction)
    print("test: ", test)
    # Gold Standard
    reference = [0, 5, 0, 0, 0, 2, 2, 2, 3, 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 0, 2, 5]
    print("reference: ", reference)

    # Evaluation
    print("rand_score: ", adjusted_rand_score(reference, test))

if __name__ == "__main__":
    main()

