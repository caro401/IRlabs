# functions for working out tf, idf, tf/idf

import math, queries

def tf(term, doc):
    # work out the frequency of the given term in the given document
    # TODO this!
    pass


def idf(term, index, num_docs=1000):
    # calculate the inverted document frequency of a given term, defaults to 1000 since 1000 docs in our data
    # idf defined as log_10 N/(df_t)
    df = len(queries.simple_query(term, index))
    return math.log((num_docs/df), 10)
    
    
def tfidf(term, doc, index):
    # calculate the tf/idf 
    pass
    
    
    