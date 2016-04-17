import math


# Simple query fuction:

def simple_query(q, inverted_index):
    # query the inverted index for a query q, expected to be a single word
    try:
        return inverted_index[q]
    except KeyError:
        return "Query is not in the dictionary. "
# print(simple_query(uni_query))
    

# bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")

def inter_queries(q, inverted_index):
    # function for finding the intersection of two query terms
    a = q.find(" ")
    q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
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
    b = q.find(" AND ")
    while b != -1:
        q = q[:b]+q[b:b+4].lower()+q[b+4]
        b += 5
        b = q.find(" AND ")
    print(q, "Here")
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
# it walks through the two lists at the same time and update the "pointers"
# bi_queries = input("Intersection of two queries, please seperate your queries with AND, ex. school AND kid: ")

def inter_queries_re(q, inverted_index):
    # revised version of inter_queries() with manual comparison of postings lists, to see steps in intersection process
    a = q.find(" ")
    q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
    a = q.find(" and ") # the space is included so that it can take "and" as queries
    if a != -1:
        word1 = q[:a]
        word2 = q[a+5:]
        lst1 = simple_query(word1, inverted_index)
        lst2 = simple_query(word2, inverted_index)
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
def inter_queries_op(q, inverted_index):
    a = q.find(" ")
    q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
    a = q.find(" and ") # the space is included so that it can take "and" as queries
    if a != -1:
        word1 = q[:a]
        word2 = q[a+5:]
        lst1 = simple_query(word1, inverted_index)
        lst2 = simple_query(word2, inverted_index)
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

def inter_queries_op_2(q, inverted_index):
    a = q.find(" ")
    q = q[:a]+q[a:a+4].lower()+q[a+4:] # just lower "AND"
    a = q.find(" and ") # the space is included so that it can take "and" as queries
    if a != -1:
        word1 = q[:a]
        word2 = q[a+5:]
        lst1 = simple_query(word1, inverted_index)
        lst2 = simple_query(word2, inverted_index)
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

        
        
if __name__ == "__main__":
    # do some testy stuff :)
    pass
