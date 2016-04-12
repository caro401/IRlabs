
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

# find the 10 most frequent words
stop_words = list()
# for word in inverted_index:

print("Stopwords: ")
print(stop_words)

query = input("Query: ")

