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
        index = create_index.make_index(filename)  # this is a tuple!
        # print(index)  # for debugging, remove later!
        if stop_num != 0:
            create_index.remove_stopwords(index, stop_num)
            # NOTE this doesn't actually remove the words from the index. 
        index = index[0]  # we don't care about the size of the index anymore so turn it into just a dictionary
            
    elif style == "db":
        # TODO Magdalena, how do we do this? 
        pass
    
    else:
        print("I don't understand, and Caroline hates error handling. Bye!")  #TODO real error handling...
        return
    
    
    
    nxt = input("What would you like to do next? Type\n    'q' for a  query\n    'tf' for a term frequency\n    'idf' for an inverted document frequency\n    'tf/idf' for a TF/IDF value\nchoice: ")
    
    if nxt == "q":
        query = input("Please type your query (case-sensitive), using 'AND' to denote conjunction: ") # Should we convert everything into lowercase?
        query_words = query.split(" ")
        if len(query_words) == 1:  # ie a single word
            print(queries.simple_query(query, index))
        elif len(query_words) == 3:  # ie conjunction of 2 words
            opt = input("What kind of function would you like to use? Type\n    's' for using the function with set\n    'n' for normal walk through\n    'o' for optimized version with skip pointers\nchoices: ")
            if opt =='s':
                print(queries.inter_queries(query, index))
            elif opt =='n':
                print(queries.inter_queries_re(query, index))
            elif opt =='o':
                print(queries.inter_queries_op(query, index))
            else:
                print("Invalid input, please try again") # TODO proper error handling message
        elif len(query_words) >= 5:  # ie conjunction of 3 or more words
            print(queries.inter_many_queries(query, index))  # TODO make this work with optimisation option Errr we don't have such thing... only conj of 2 words has it
    
    elif nxt == "tf":
        pass
    
    elif nxt == "idf":
        pass
    
    elif nxt == "tf/idf":
        pass
    else:
        print("Invalid input, please try again") # TODO proper error message


    
if __name__ == "__main__":
    main()
