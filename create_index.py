# This is Chiao-ting's code originally at the start of lab1.py


def make_index(filename):
    # create and fill inverted index
    # inverted index is a dictionary with words as keys, mapping to a list of associated documents
    inverted_index = dict()
    num_postings = 0
    with open(filename, "r", encoding="utf8") as fobj:  # TODO error handling here ugh
        for line in fobj:
            num_postings += 1
            word, document = line.split()
            if word not in inverted_index:
                inverted_index[word] = list()
            inverted_index[word].append(int(document))
    
    print("File Imported. Basic inverted index created. ")
    print(len(inverted_index), " entries in dictionary.")
    print(num_postings, " total postings.")
    return (inverted_index, num_postings)
    

def remove_stopwords(index, stop_num):
    # find the stop_num most frequent words and make them the stop words
    # stop_words is a list with stop_num tuples in the form of (frequecy, word)
    # index expected to be a tuple (dict, int) of the inverted index and its number of postings, as returned by make_index()
    # stop_num expected to be an int, the number of words to be removed
    stop_words = list()
    for key, value in index[0].items():
        stop_words.append((len(value), key))
    
    stop_words.sort(reverse=True)
    print("Stopwords: ")
    print(stop_words[:stop_num])
    
    # update the size of total entries and postings after removing all the stop words
    print(len(index[0])-stop_num, "entries in dictionary after the stop words are removed. ")
    stop_words_postings = 0
    for key, value in stop_words[:stop_num]:
        stop_words_postings += key
    print(index[1]-stop_words_postings, "total postings after the stop words are removed. ")