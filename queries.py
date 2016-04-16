import math


# Simple query fuction:
# uni_query = input("Simple query, please enter a word: ")

def simple_query(q, inverted_index):
    # query the inverted index for a query q, expected to be a single word
    q = q.lower()
    try:
        return inverted_index[0][q]
    except KeyError:
        return "Query is not in the dictionary. "
# print(simple_query(uni_query))
    

# bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")

def inter_queries(q, inverted_index):
    # function for finding the intersection of two query terms
    q = q.lower()
    a = q.find(" and ") # the space is included so that it can take "and" as queries
    if a != -1:
        word1 = q[:a]
        word2 = q[a+5:]
        lst1 = simple_query(word1, inverted_index)
        lst2 = simple_query(word2, inverted_index)
        inter_result = sorted(list(set(lst1) & set(lst2)))
        if len(inter_result) != 0:
            return inter_result
        else:
            return "There are no entries that meet both queries. "
    else:
        return "Invalid input"

#print(inter_queries(bi_queries))


#multi_queries = input("Intersection of multiple queries, please seperate them with AND, ex. school AND kid AND really: ")

def inter_many_queries(q, inverted_index):
    # function for finding the intersection of >2 query terms
    q = q.lower()
    query_list = []
    a = qr.find(" and ")
    while a != -1: # when there are still queries left (by checking " and ")
        word = q[:a]
        query_list.append(word)
        q = q[a+5:]
        a = q.find(" and ") 
    query_list.append(q) # all the queries are appended items in this list
    
    intersections = []
    for item in query_list:  # go through each item in the query_list
        one_query_result = simple_query(item, inverted_index)  # use simple_query to find the postings for each
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
# bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")

def inter_queries_re(q, inverted_index):
    # revised version of inter_queries() with manual comparison of postings lists, to see steps in intersection process
    q = q.lower()
    a = q.find(" and ") # the space is included so that it can take "and" as queries
    if a != -1:
        word1 = q[:a]
        word2 = q[a+5:]
        lst1 = simple_query(word1, inverted_index)
        lst2 = simple_query(word2, inverted_index)
        step = 0
        inter_result = []
        for item1 in lst1:
            for item2 in lst2:
                step += 1
                if item1 == item2:
                    inter_result.append(item1)
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
# So this "optimized" version tries to skip smaller postings (see 2.3 in the textbook and check if I interpret it correctly? )
# bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")
def inter_queries_re_op(str, inverted_index):
    str = str.lower()
    a = str.find(" and ") # the space is included so that it can take "and" as queries
    if a != -1:
        word1 = str[:a]
        word2 = str[a+5:]
        lst1 = simple_query(word1, inverted_index)
        lst2 = simple_query(word2, inverted_index)
        step = 0
        inter_result = []
        skip1 = round(math.sqrt(len(lst1)))
        skip2 = round(math.sqrt(len(lst2)))
        current1 = 0
        current2 = 0
        if lst1[current1]>lst2[current2]:
            #TODO something...
            pass
            
            
        
        else:
            # TODO something...
            pass
            
        if len(inter_result) != 0:
            print("Number of steps to find the intersection: ", step)
            return inter_result
        else:
            return "There are no entries that meet both queries. "
    else:
        return "Invalid input"
        
# print(inter_queries_re_op(bi_queries))