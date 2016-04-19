# class for an inverted index represented as a python dictionary


import math, subprocess, shlex, tfidf_util

class PythonIndex:

    def __init__(self, filename):
        # create and fill inverted index
        # inverted index is a dictionary with words as keys, mapping to a list of associated documents
        self.inverted_index = dict()
        self.num_postings = 0
        self._tf = dict()
        self._docs = set()
        with open(filename, "r", encoding="utf8") as fobj:
            for line in fobj:
                word, document = line.split()
                self._docs.add(int(document))
                if word not in self._tf:
                    self._tf[word] = dict()
                if int(document) not in self._tf[word]:
                    self._tf[word][int(document)] = 0
                    self.num_postings += 1
                self._tf[word][int(document)] += 1
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
        # print("Stopwords: ")
        # print(stop_words[:stop_num])

        # update the size of total entries and postings after removing all the stop words
        print(len(self.inverted_index)-stop_num, "words in dictionary after the stop words are removed. ")
        stop_words_postings = 0
        for key, value in stop_words[:stop_num]:
            stop_words_postings += key
        print(self.num_postings-stop_words_postings, "total postings after the stop words are removed. ")

        ret = list()
        for entry in stop_words[:stop_num]:
            ret.append(entry[1])
        return ret

    def query(self, q, opt='s'):
        query_words = q.split(" ")
        if len(query_words) == 1:  # ie a single word
            return self.simple_query(q)
        elif len(query_words) >= 3:  # ie conjunction of 2 words
            if opt =='s':
                if len(query_words) > 3:
                    return self.inter_many_queries(q)
                else:
                    return self.inter_queries(q)
            elif opt =='n':
                query_result = self.inter_queries_re(q)
                print("Number of steps to find intersection:", query_result[1])
                return query_result[0]
            elif opt =='o':
                query_result = self.inter_queries_op(q)
                print("Number of steps to find intersection:", query_result[1])
                return query_result[0]
            elif opt =='2':
                query_result = self.inter_queries_op_2(q)
                print("Number of steps to find intersection:", query_result[1])
                return query_result[0]
            else:
                print("Invalid input, please try again")
            
    # Simple query fuction:
    def simple_query(self, q):
        # query the inverted index for a query q, expected to be a single word
        try:
            return self.inverted_index[q]
        except KeyError:
            return "Query is not in the dictionary. "

    def inter_queries(self, q):
        # function for finding the intersection of two query terms
        #a = q.find(" ")
        #q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
        a = q.find(" AND ") # the space is included so that it can take "and" as queries
        if a != -1: 
            word1 = q[:a]
            word2 = q[a+5:]
            lst1 = self.simple_query(word1)
            lst2 = self.simple_query(word2)
            inter_result = sorted(list(set(lst1) & set(lst2))) # use set to get the intersection of two queries
            if len(inter_result) != 0:
                return inter_result
            else:
                return "There are no entries that meet both queries. "
        else:
            return "Invalid input"

    def inter_many_queries(self, q): # this function is not case-sensitive
        # function for finding the intersection of >2 query terms
        #q = q.lower() 
        a = q.find(" AND ")
        query_list = []
        while a != -1: # when there are still queries left (by checking " and ")
            word = q[:a]
            query_list.append(word)
            q = q[a+5:]
            a = q.find(" AND ")
        query_list.append(q) # all the queries are appended to this list

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


# Adjust your query processing routines to return the number of comparisons needed to perform the intersections.
# Since we are using sets, we can't really see how many steps it takes to do the comparison. So here is a "revised" version of the inter_queries function
# it walks through the two lists at the same time and update the "pointers"
# bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")

    def inter_queries_re(self, q):
        # revised O(m+n) version of inter_queries() showing how many comparison steps there are
        #a = q.find(" ")
        # q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
        a = q.find(" AND ") # the space is included so that it can take "and" as queries
        if a != -1:
            word1 = q[:a]
            word2 = q[a+5:]
            lst1 = self.simple_query(word1)
            word2_a = q.find(" AND ")
            if word2_a != -1:
                lst2, step = self.inter_queries_re(word2)
            else:
                lst2 = self.simple_query(word2)
                step = 0 # for counting the step
            inter_result = [] # the intersection of the posting will be appended here
            current1 = 0 # pointer for lst1
            current2 = 0 # pointer for lst2
            while current1 <= len(lst1)-1 and current2 <= len(lst2)-1: # when both have not reach the end of the list
                if lst1[current1] == lst2[current2]: # if found in both, increase step, append, and move pointer. 
                    step += 1
                    inter_result.append(lst1[current1])
                    current1 += 1
                    current2 += 1
                elif lst1[current1] < lst2[current2]: # if the current item in lst1 is smaller, increase step and current1
                    step += 1
                    current1 += 1
                else: # lst1[current1] > lst2[current2], increase step and current2 
                    step += 1
                    current2 += 1
            # print("Number of steps to find the intersection: ", step)
            return inter_result, step
        else:
            return self.simple_query(q), 0

    # ""Add a simple query optimization feature and measure the number of comparison steps after adding this feature.""
    # It is actually not very effcient to compare each and every item in both lists as they are in order.
    # So this "optimized" version tries to skip smaller postings by checking ahead
    # Unlike the skip points which occur every sqrt(len(lst)) items, this check the skip pointer for every item.
    # bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")
    def inter_queries_op(self, q):
        #a = q.find(" ")
        #q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
        a = q.find(" AND ") # the space is included so that it can take "and" as queries
        if a != -1:
            word1 = q[:a]
            word2 = q[a+5:]
            lst1 = self.simple_query(word1)
            word2_a = q.find(" AND ")
            if word2_a != -1:
                lst2, step = self.inter_queries_op(word2)
            else:
                lst2 = self.simple_query(word2)
                step = 0 # for counting the step
            inter_result = [] # the intersection goes here
            skip1 = round(math.sqrt(len(lst1))) # the skip gap is the square root of the length of the list
            skip2 = round(math.sqrt(len(lst2))) 
            current1 = 0 # pointer for lst1
            current2 = 0 # pointer for lst2 
            while current1 <= len(lst1)-1 and current2 <= len(lst2)-1: # when both have not reach the end of the lists
                if lst1[current1] == lst2[current2]:  # if the item occurs in both lists, increase step, add item to result, move both pointers
                    step += 1 
                    inter_result.append(lst1[current1])
                    current1 += 1
                    current2 += 1
                elif lst1[current1] < lst2[current2]: # if the current item in lst1 is smaller
                    step += 1 # increase step
                    if current1+skip1 <= len(lst1)-1: # if the current point plus the gap to skip pointer is within the list length 
                        if lst1[current1+skip1] < lst2[current2]: # check if the skip pointer in lst1 will still be smaller than item in lst2 
                            current1 += skip1 # if yes, increase current1 with the gap
                    current1 += 1 # if not, just increase pointer by 1
                else: # lst1[current1] > lst2[current2] (if the current item in lst2 is smaller)
                    step += 1 # increase step
                    if current2+skip2 <= len(lst2)-1: # if the current point plus the gap to skip pointer is within the list length 
                        if lst1[current1] > lst2[current2+skip2]: # check if the skip pointer in lst2 will still be smaller than item in lst1
                            current2 += skip2 # if yes, increase current2 with the gap
                    current2 += 1 # if not, just increase pointer by 1
            return inter_result, step
        else:
            return self.simple_query(q), 0

# The function above checks skip point for every item and decides if a skip is needed.
# But according to the textbook (P.34) only a number of the postings have skip pointers that can jump ahead, others still increase gradually.
# This function here works with fixed skip pointers, only items in the item_skip lists will be checked when needed.

    def inter_queries_op_2(self, q):
        #a = q.find(" ")
        #q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
        a = q.find(" AND ") # the space is included so that it can take "and" as queries
        if a != -1:
            word1 = q[:a]
            word2 = q[a+5:]
            lst1 = self.simple_query(word1)
            word2_a = q.find(" AND ")
            if word2_a != -1:
                lst2, step = self.inter_queries_op_2(word2)
            else:
                lst2 = self.simple_query(word2)
                step = 0 # for counting the step
            inter_result = []
            skip1 = round(math.sqrt(len(lst1)))
            skip2 = round(math.sqrt(len(lst2)))
            current1 = 0
            current2 = 0
            item_skip1 = [] # list of items with skip pointers in lst1 
            item_skip2 = [] # list of items with skip pointers in lst2 
            for i in range(0, len(lst1), skip1): # append items with skip1 as gap
                item_skip1.append(lst1[i])
            for i in range(0, len(lst2), skip2): # append items with skip2 as gap
                item_skip2.append(lst2[i])
            while current1 <= len(lst1)-1 and current2 <= len(lst2)-1: # when both lists have not reach the end
                if lst1[current1] == lst2[current2]:
                    step += 1
                    inter_result.append(lst1[current1])
                    current1 += 1
                    current2 += 1
                elif lst1[current1] < lst2[current2]: # if current item in lst1 is smaller than the current in lst2
                    step += 1
                    if lst1[current1] in item_skip1[:-1]: # if current item has skip pointer, but is not the last item in the item_skip1 list (can't skip to next if it is the last one)
                        if lst1[current1+skip1] < lst2[current2]: # if current will still be smaller than item in lst2 after skip
                            current1 += skip1 # then skip
                        else: # if not, just increase by 1
                            current1 +=1
                    else:
                        current1 += 1
                else: # lst1[current1] > lst2[current2]
                    step += 1
                    if lst2[current2] in item_skip2[:-1]: # if current item has skip pointer and is not the last in item_skip2 list
                        if lst1[current1] > lst2[current2+skip2]: # if current will still be smaller than item in lst1 after skip  
                            current2 += skip2 # then skip
                        else: # if not, just increase by 1
                            current2 += 1 
                    else: # lst1[current1] < lst2[current2+skip2], do not skip, just increase 1
                        current2 += 1

            return inter_result, step
        else:
            return self.simple_query(q), 0
    
    

# functions for final part of assignment

    def tf(self, term, doc):
        return self._tf[term][doc]

    def idf(self, term):
        # calculate the inverted document frequency of a given term, defaults to 1000 since 1000 docs in our data (i think... should probably check this)
        # idf defined as log_10 N/(df_t)
        df = len(self.simple_query(term))
        return math.log((len(self._docs)/df), 10)
        
        
    def tfidf(self, term, doc_id):
        # calculate the tf/idf 
        # using the definition given in the lecture slides
        tf = self.tf(term, doc_id)
        idf = self.idf(term)
        return tf*idf

    
    def compute_sim(self, query_str): 
        # find all the docs matching query, assumiung this will be lowercased already
        doc_list = self.query(query_str) 
        
        # compute vector of tf/idf for query terms
        query_terms = query_str.split(" AND ")
        query_vector = []  # compute tf/idf for each term in query wrt query in here
        # going to assume unique query terms, so raw tf = 1, scaled tf = 1 + log_10(1) = 1
        for term in query_terms:
            query_vector.append(self.idf(term))
        
        scores = []  # this will be a list of tuples (doc-id, cosine-sim)
        
        # compute vector of tf/idf weights for each document, then calculate cosine similarity between document and query vectors
        for doc in doc_list:
            doc_vector = []
            for term in query_terms:
                doc_vector.append(self.tfidf(term, doc)) # compute vector of tf/idf of all query
            sim = tfidf_util.cosine_sim(query_vector, doc_vector) # compute cosine_sim of that vector with the query vector
            scores.append((doc, sim))
        
        # rank docs according to similarity
        scores = sorted(scores, key=lambda x: x[1])  # sort the list of tuples on the cosine sim
        #TODO check this comes out in the right order!
        
        # return ordered list of docs
        ordered_docs =  [x[0] for x in scores]  # I hope this will give you a list consisting just of the first bit of each tuple, ie the docID
        return ordered_docs
        
