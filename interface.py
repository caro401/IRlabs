# this is the main file, run this to call all the functions you wrote elsewhere
#TODO error handling zzzzz
import  create_index, queries, tfidf #, lab1_sqlite


def main():
    print("Code for Information Retrieval Lab 1 by Chiao-ting Fang, Magdalena Parks & Caroline Appleby")
    style = input("Would you like to use a Python dictionary or a SQLite database? Type 'dict' or 'db': ")
    filename = input("Create an inverted index! Please input the filename: ")
    stop = input("How many stop words would you like? Please enter a number: ")
    
    try: 
        stop_num = int(stop)
    except ValueError:
        print("Not a valid number, defaulting to 10")
        stop_num = 10 
    
    if style == "dict":
        index = create_index.make_index(filename)
        # print(index)  # for debugging, remove later!
        if stop_num != 0:
            create_index.remove_stopwords(index, stop_num)
            # NOTE this doesn't actually remove the words from the index. TODO should it? 
            
    elif style == "db":
        # TODO Magdalena, how do we do this? 
        pass 
    
    else:
        print("I don't understand, and Caroline hates error handling. Bye!")  #TODO real error handling...
        return
    
    
    
    nxt = input("What would you like to do next? Type\n    'q' for a  query\n    'tf' for a term frequency\n    'idf' for an inverted document frequency\n    'tf/idf' for a TF/IDF value\nchoice: ")
    
    if nxt == "q":
        query = input("Please type your query, using 'AND' to denote conjunction: ")
        opt = input("Would you like to use the optimized query function? Type 'y' or 'n': ")  #TODO make this do something...
        query_words = query.split(" ")
        if len(query_words) == 1:  # ie a single word
            print(queries.simple_query(query, index))
        elif len(query_words) == 3:  # ie conjunction of 2 words
            print(queries.inter_queries(query, index))
        elif len(query_words) >= 5:  # ie conjunction of 3 or more words
            print(queries.inter_many_queries(query, index))  # TODO make this work with optimisation option
    
    elif nxt == "tf":
        pass
    
    elif nxt == "idf":
        pass
    
    elif nxt == "tf/idf":
        pass


    
if __name__ == "__main__":
    main()
