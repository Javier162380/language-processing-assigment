import os, numpy
import nltk
from nltk.corpus import stopwords
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.cluster import adjusted_rand_score

def filter_stopwords(token_list):
    stop = set(stopwords.words('english'))
    clean_tokens = []
    for token in token_list:
        if token[0] not in stop:
            clean_tokens.append(token)
    return clean_tokens

def process_text(text):
    chunk_tokens =  nltk.ne_chunk(nltk.pos_tag(text.split()))
    nltk_chunks = [" ".join(w for w, t in entidad_nombrada) for entidad_nombrada in chunk_tokens
                   if isinstance(entidad_nombrada,  nltk.Tree)
                   and hasattr(entidad_nombrada, 'label') and (entidad_nombrada.label()=='PERSON'
                   or entidad_nombrada.label()=='GPE' or entidad_nombrada.label()=='GPS')]

    nltk_chunks_erase_stop_words = filter_stopwords(nltk_chunks)
    return nltk_chunks_erase_stop_words

def cluster_texts(texts, clustersNumber, distance):
    #Load the list of texts into a TextCollection object.
    collection = nltk.TextCollection(texts)
    print("Created a collection of {0}, terms.".format(len(collection)))
    #get a list of unique terms
    unique_terms = list(set(collection))
    print("Unique terms found: ", len(unique_terms))
    ### And here we actually call the function and create our array of vectors.
    vectors_tf_idf = [numpy.array(TF_IDF(f,unique_terms, collection)) for f in texts]

    vectors_idf = [numpy.array(IDF(f, unique_terms, collection)) for f in texts]
    print("Vectors created.")
    # initialize the clusterer
    cluster = AgglomerativeClustering(n_clusters=clustersNumber,
                                      linkage="average", affinity=distance)
    clusters_tfidf = cluster.fit_predict(vectors_tf_idf)
    clusters_idf = cluster.fit_predict(vectors_idf)
    return (clusters_tfidf,clusters_idf)

# Function to create a TF vector for one document. For each of
# our unique words, we have a feature which is the tf for that word
# in the current document
def TF_IDF(document, unique_terms, collection):
    word_tf = []
    for word in unique_terms:
        word_tf.append(collection.tf_idf(word,document))
    return word_tf

def IDF(document,unique_terms, collection):
    word_tf = []
    for word in unique_terms:
        word_tf.append(collection.idf(word))
    return word_tf

def main():
    folder = "/Txt/"
    abs_path=os.path.dirname(os.path.realpath(__file__))+folder
    # Empty list to hold text documents.
    texts = []
    listing = os.listdir(abs_path)
    for file in sorted(listing):
        if file.endswith(".txt"):
            url = abs_path+file
            f = open(url, encoding="utf-8" ,errors='ignore')
            raw = f.read()
            f.close()
            texts.append(process_text(raw))

    print("Prepared {0},  documents...".format(len(texts)))
    print("They can be accessed using texts[0] - texts[ {0}".format(str(len(texts) - 1))+"]")
    distanceFunctions = ["euclidean","braycurtis","cosine"]

    for i in distanceFunctions:
        test = cluster_texts(texts, 5, i)
        print("test_tfidf: ", test[0])
        print("test_idf: ", test[1])
        ## Gold Standard
        reference = [0, 5, 0, 0, 0, 2, 2, 2, 3, 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 0, 2, 5]
        print("reference: ", reference)
        ## Evaluation
        print("resultados para la distancia {0}".format(i))
        print("rand_score_tfidf: ", adjusted_rand_score(reference, test[0]))
        print("rand_score_idf: ", adjusted_rand_score(reference, test[1]))
if __name__ == "__main__":
    main()