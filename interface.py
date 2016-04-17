# this is the main file, run this to call all the functions you wrote elsewhere
#TODO error handling zzzzz
import tfidf, python_index, sql_index


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
        index = python_index.PythonIndex(filename)
    elif style == "db":
        index = sql_index.SQLIndex(filename)
        pass
    
    else:
        print("I don't understand, and Caroline hates error handling. Bye!")  #TODO real error handling...
        return

    print("File Imported. Basic inverted index created. ")
    print(index.get_num_words(), " entries in dictionary.")
    print(index.get_num_postings(), " total postings.")
    print("Stop Words: ")
    print(index.get_stop_words(stop_num))

    
    nxt = input("What would you like to do next? Type\n    'q' for a  query\n    'tf' for a term frequency\n    'idf' for an inverted document frequency\n    'tf/idf' for a TF/IDF value\n    'cos' for cosine similarity\nchoice: ")
    
    if nxt == "q":
        query = input("Please type your query, using 'AND' to denote conjunction: ")
        print(index.query(query))

    elif nxt == "tf":
        term = input("Please enter the term: ")
        doc = int(input("Please enter the document ID number: "))
        print(tfidf.tf(term, doc))
        
    
    elif nxt == "idf":
        term = input("Please enter the term: ")
        print(tfidf.idf(term, index))
        
    
    elif nxt == "tf/idf":
        term = input("Please enter the term: ")
        doc = int(input("Please enter the document ID number: "))
        print(tfidf.tfidf(term, doc, index))
        
    else:
        print("Invalid input, please try again") # TODO proper error message


    
if __name__ == "__main__":
    main()
