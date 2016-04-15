
filename = input("Please input the filename: ")

# create and fill inverted index
# inverted index is a dictionary with words as keys, mapping to a list of associated documents
inverted_index = dict()
num_postings = 0
with open(filename, "r", encoding="utf8") as fobj:
    for line in fobj:
        num_postings += 1
        word, document = line.split()
        if word not in inverted_index:
            inverted_index[word] = list()
        inverted_index[word].append(int(document))

print("File Imported. ")
print(len(inverted_index), " entries in dictionary.")
print(num_postings, " total postings.")

# find the 10 most frequent words and make them the stop words
# stop_words is a list with ten tuples in the form of (frequecy, word) 
stop_num = input("How many stop words do you want to exclude? Default value is 10. ")
try: 
    stop_num = int(stop_num)
except ValueError:
    stop_num = 10 
stop_words = list()
for key, value in inverted_index.items():
    stop_words.append((len(value), key))

stop_words.sort(reverse=True)
print("Stopwords: ")
print(stop_words[:stop_num])

# update the size of total entries and postings after removing all the stop words
print(len(inverted_index)-stop_num, "entries in dictionary after the stop words are removed. ")
stop_words_postings = 0
for key, value in stop_words[:stop_num]:
    stop_words_postings += key
print(num_postings-stop_words_postings, "total postings after the stop words are removed. ")

# Simple query fuction:
uni_query = input("Simple query, please enter a word: ")

def simple_query(str):
    try:
        return inverted_index[str]
    except KeyError:
        return "Query is not in the dictionary. "
print(simple_query(uni_query))
    
# function for finding the intersection of two queries
bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")

def inter_queries(str):
    a = bi_queries.find(" AND ")
    if a == -1:
        a = bi_queries.find(" and ") # is there a more pythonic way to allow both "AND" and "and"?
    if a != -1:
        word1 = bi_queries[:a]
        word2 = bi_queries[a+5:]
        lst1 = simple_query(word1)
        lst2 = simple_query(word2)
        inter_result = sorted(list(set(lst1) & set(lst2)))
        if len(inter_result) != 0:
            return inter_result
        else:
            return "There are no entries that meet both of the queries. "
    else:
        return "Invalid input"

print(inter_queries(bi_queries))
        
        
