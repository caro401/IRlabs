# functions for working out tf, idf, tf/idf
# not at all tested yet

import math, queries, subprocess

def tf(term, doc):
    # work out the frequency of the given term in the given document
    # assume existence of doc tf_lc.txt, as made in section 3 of task
    # columns: freq, term, doc, separated by spaces? check this, and test
    query = "grep " + term + " " + str(doc) + " tf_lc.txt"  # TODO some kind of safety check? cos shell injection...
    line = subprocess.check_output(query, shell=True)  # using grep for speed in a huge file
    cols = line.split(" ")
    return cols[0]  # because the count of that term in that doc is the value in the first col


def idf(term, index, num_docs=1000):
    # calculate the inverted document frequency of a given term, defaults to 1000 since 1000 docs in our data (i think... should probably check this)
    # idf defined as log_10 N/(df_t)
    df = len(queries.simple_query(term, index))
    return math.log((num_docs/df), 10)
    
    
def tfidf(term, doc, index):
    # calculate the tf/idf 
    # using the definition given in the lecture slides
    tf = tf(term, doc)
    idf = idf(term, index)
    return tf*idf
    
def cosine_sim(doc1, doc2):
    # actually i have no idea what this is meant to do
    # TODO this
    pass
    