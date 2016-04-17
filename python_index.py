# This is Chiao-ting and Magdalena's code originally at the start of lab1.py

import math, subprocess

class PythonIndex:

    def __init__(self, filename):
        # create and fill inverted index
        # inverted index is a dictionary with words as keys, mapping to a list of associated documents
        self.inverted_index = dict()
        self.num_postings = 0
        with open(filename, "r", encoding="utf8") as fobj:  # TODO error handling here ugh
            for line in fobj:
                self.num_postings += 1
                word, document = line.split()
                if word not in self.inverted_index:
                    self.inverted_index[word] = list()
                self.inverted_index[word].append(int(document))

    def get_num_words(self):
        return len(self.inverted_index)

    def get_num_postings(self):
        return self.num_postings

    def get_stop_words(self, stop_num):
        # find the stop_num most frequent words and make them the stop words
        # stop_words is a list with stop_num tuples in the form of (frequecy, word)
        # index expected to be a tuple (dict, int) of the inverted index and its number of postings, as returned by make_index()
        # stop_num expected to be an int, the number of words to be removed
        stop_words = list()
        for key, value in self.inverted_index.items():
            stop_words.append((len(value), key))

        stop_words.sort(reverse=True)
        print("Stopwords: ")
        print(stop_words[:stop_num])

        # update the size of total entries and postings after removing all the stop words
        print(len(self.inverted_index)-stop_num, "entries in dictionary after the stop words are removed. ")
        stop_words_postings = 0
        for key, value in stop_words[:stop_num]:
            stop_words_postings += key
        print(self.num_postings-stop_words_postings, "total postings after the stop words are removed. ")

    def query(self, q):
        query_words = q.split(" ")
        if len(query_words) == 1:  # ie a single word
            return self.simple_query(q)
        elif len(query_words) == 3:  # ie conjunction of 2 words
            opt = input("What kind of function would you like to use? Type\n    's' for using the function with set\n    'n' for normal walk through\n    'o' for optimized version with skip pointers for every step\n    '2' for optimized version with fixed skip pointers\nchoices: ")
            if opt =='s':
                return self.inter_queries(q)
            elif opt =='n':
                return self.inter_queries_re(q)
            elif opt =='o':
                return self.inter_queries_op(q)
            elif opt =='2':
                return self.inter_queries_op_2(q)
            else:
                print("Invalid input, please try again") # TODO proper error handling message
        elif len(query_words) >= 5:  # ie conjunction of 3 or more words
            return self.inter_many_queries(q)  # TODO make this work with optimisation option Errr we don't have such thing... only conj of 2 words has it

    # Simple query fuction:
    def simple_query(self, q):
        # query the inverted index for a query q, expected to be a single word
        try:
            return self.inverted_index[q]
        except KeyError:
            return "Query is not in the dictionary. "
    # print(simple_query(uni_query))

    def inter_queries(self, q):
        # function for finding the intersection of two query terms
        a = q.find(" ")
        q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
        a = q.find(" and ") # the space is included so that it can take "and" as queries
        if a != -1:
            word1 = q[:a]
            word2 = q[a+5:]
            lst1 = self.simple_query(word1)
            lst2 = self.simple_query(word2)
            inter_result = sorted(list(set(lst1) & set(lst2)))
            if len(inter_result) != 0:
                return inter_result
            else:
                return "There are no entries that meet both queries. "
        else:
            return "Invalid input"

    def inter_many_queries(self, q):
        # function for finding the intersection of >2 query terms
        q = q.lower()
        a = q.find(" and ")
        query_list = []
        while a != -1: # when there are still queries left (by checking " and ")
            word = q[:a]
            query_list.append(word)
            q = q[a+5:]
            a = q.find(" and ")
        query_list.append(q) # all the queries are appended items in this list

        intersections = []
        for item in query_list:  # go through each item in the query_list
            one_query_result = self.simple_query(item)  # use simple_query to find the postings for each
            intersections.append(one_query_result) # add the posting list as an element in the intersections list (which will be compared later)
        result = set(intersections[0]) & set(intersections[1]) # the intersection of the first two queries
        for i in range(len(intersections)-2): # get other intersections based on the intersection of first two
            result = result & set(intersections[i+2])
        result = sorted(list(result))
        if len(result) > 0:
            return result
        else:
            return "There are no entries that meet all the queries."


#print(inter_many_queries(multi_queries))

# Adjust your query processing routines to return the number of comparisons needed to perform the intersections.
# Since we are using sets, we can't really see how many steps it takes to do the comparison. So here is a "revised" version of the inter_queries function
# it walks through the two lists at the same time and update the "pointers"
# bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")

    def inter_queries_re(self, q):
        # revised version of inter_queries() with manual comparison of postings lists, to see steps in intersection process
        a = q.find(" ")
        q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
        a = q.find(" and ") # the space is included so that it can take "and" as queries
        if a != -1:
            word1 = q[:a]
            word2 = q[a+5:]
            lst1 = self.simple_query(word1)
            lst2 = self.simple_query(word2)
            step = 0
            inter_result = []
            current1 = 0
            current2 = 0
            while current1 <= len(lst1)-1 and current2 <= len(lst2)-1:
                if lst1[current1] == lst2[current2]:
                    step += 1
                    inter_result.append(lst1[current1])
                    current1 += 1
                    current2 += 1
                elif lst1[current1] < lst2[current2]:
                    step += 1
                    current1 += 1
                else: # lst1[current1] > lst2[current2]
                    step += 1
                    current2 += 1
            if len(inter_result) != 0:
                print("Number of steps to find the intersection: ", step)
                return inter_result
            else:
                return "There are no entries that meet both queries. "
        else:
            return "Invalid input"

    # print(inter_queries_re(bi_queries))

    #Add a simple query optimization feature and measure the number of comparison steps after adding this feature.
    # It is actually not very effcient to compare each and every item in both lists as they are in order.
    # So this "optimized" version tries to skip smaller postings by checking ahead
    # Unlike the skip points which occur every 3-4 items, this check the skip pointer for every item.
    # bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")
    def inter_queries_op(self, q):
        a = q.find(" ")
        q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
        a = q.find(" and ") # the space is included so that it can take "and" as queries
        if a != -1:
            word1 = q[:a]
            word2 = q[a+5:]
            lst1 = self.simple_query(word1)
            lst2 = self.simple_query(word2)
            step = 0
            inter_result = []
            skip1 = round(math.sqrt(len(lst1)))
            skip2 = round(math.sqrt(len(lst2)))
            current1 = 0
            current2 = 0
            while current1 <= len(lst1)-1 and current2 <= len(lst2)-1:
                if lst1[current1] == lst2[current2]:
                    #print(lst1[current1], lst2[current2])
                    step += 1
                    inter_result.append(lst1[current1])
                    current1 += 1
                    current2 += 1
                elif lst1[current1] < lst2[current2]:
                    #print(lst1[current1], lst2[current2])
                    step += 1
                    if current1+skip1 <= len(lst1)-1:
                        if lst1[current1+skip1] < lst2[current2]:
                            #print(lst1[current1+skip1], lst2[current2])
                            current1 += skip1
                    current1 += 1
                else: # lst1[current1] > lst2[current2]
                    #print(lst1[current1], lst2[current2])
                    step += 1
                    if current2+skip2 <= len(lst2)-1:
                        if lst1[current1] > lst2[current2+skip2]:
                            #print(lst1[current1], lst2[current2+skip2])
                            current2 += skip2
                    # lst1[current1] < lst2[current2+skip2], do not skip
                    current2 += 1

            if len(inter_result) != 0:
                print("Number of steps to find the intersection: ", step)
                return inter_result
            else:
                return "There are no entries that meet both queries. "
        else:
            return "Invalid input"

    # print(inter_queries_re_op(bi_queries))

    def inter_queries_op_2(self, q):
        a = q.find(" ")
        q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
        a = q.find(" and ") # the space is included so that it can take "and" as queries
        if a != -1:
            word1 = q[:a]
            word2 = q[a+5:]
            lst1 = self.simple_query(word1)
            lst2 = self.simple_query(word2)
            step = 0
            inter_result = []
            skip1 = round(math.sqrt(len(lst1)))
            skip2 = round(math.sqrt(len(lst2)))
            current1 = 0
            current2 = 0
            item_skip1 = []
            item_skip2 = []
            for i in range(0, len(lst1), skip1):
                item_skip1.append(lst1[i])
            for i in range(0, len(lst2), skip2):
                item_skip2.append(lst2[i])
            while current1 <= len(lst1)-1 and current2 <= len(lst2)-1:
                if lst1[current1] == lst2[current2]:
                    #print(lst1[current1], lst2[current2])
                    step += 1
                    inter_result.append(lst1[current1])
                    current1 += 1
                    current2 += 1
                elif lst1[current1] < lst2[current2]:
                    #print(lst1[current1], lst2[current2])
                    step += 1
                    if lst1[current1] in item_skip1[:-1]:
                        if lst1[current1+skip1] < lst2[current2]:
                            #print(lst1[current1+skip1], lst2[current2])
                            current1 += skip1
                        else:
                            current1 +=1
                    else:
                        current1 += 1
                else: # lst1[current1] > lst2[current2]
                    #print(lst1[current1], lst2[current2])
                    step += 1
                    if lst2[current2] in item_skip2[:-1]:
                        if lst1[current1] > lst2[current2+skip2]:
                            #print(lst1[current1], lst2[current2+skip2])
                            current2 += skip2
                        else:
                            current2 += 1
                    else: # lst1[current1] < lst2[current2+skip2], do not skip
                        current2 += 1

            if len(inter_result) != 0:
                print("Number of steps to find the intersection: ", step)
                return inter_result
            else:
                return "There are no entries that meet both queries. "
        else:
            return "Invalid input"
    
    def idf(self, term, num_docs=1000):
        # calculate the inverted document frequency of a given term, defaults to 1000 since 1000 docs in our data (i think... should probably check this)
        # idf defined as log_10 N/(df_t)
        df = len(self.simple_query(term))
        return math.log((num_docs/df), 10)
        
        
    def tfidf(self, term, doc):
        # calculate the tf/idf 
        # using the definition given in the lecture slides
        tf = tf(term, doc)
        idf = self.idf(term, self.inverted_index)
        return tf*idf

    
    def compute_sim(self, query):  # TODO!
        # find all the docs matching query
        
        # compute vector of tf/idf for query terms
        # for all docs
            # compute vector of tf/idf of all query 
            # compute cosine_sim of that vector with the query vector
        # rank docs according to similarity
        # return ordered list of docs
        pass
        


def dot_prod(v1, v2):
    # calculate the dot product of 2 vectors, represented as arrays
    if len(v1) != len(v2):
        print("Dot product undefined over vectors of different dimensions")
        return None
    total = 0
    for i in range(len(v1)):
        total += v1[i] * v2[i]
    return total
    
    
def cosine_sim(v1, v2):
    # compute the cosine similarity of 2 vectors
    sim = dot_prod(v1, v2) / (math.sqrt(dot_prod(v1, v1)) * math.sqrt(dot_prod(v2, v2)))  # this works because (v1.v1) = v1^2
    return sim
    

def tf(term, doc):
        # work out the frequency of the given term in the given document
        # assume existence of doc tf_lc.txt, as made in section 3 of task
        # columns: freq, term, doc, separated by spaces? check this, and test
        query = 'grep "' + term + "\t" + str(doc) + '" term_frequency.txt'  # TODO some kind of safety check? cos shell injection...
        try:
            line = subprocess.check_output(query, shell=True)  # using grep for speed in a huge file
        except:  # grep didn't find the term and document combination you are looking for
            return 0   
        cols = line.decode('utf-8').split("\t")
        print("raw freq: ", cols[0])
        return 1 + math.log(int(cols[0]), 10)  # because the count of that term in that doc is the value in the first column of file
    
    
if __name__ == "__main__":
    # do some testy stuff :)
    pass