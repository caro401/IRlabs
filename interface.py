# this is the main file, run this to call all the functions you wrote elsewhere
#TODO error handling zzzzz
import python_index, sql_index


def main():
    print("Code for Information Retrieval Lab 1 by Chiao-ting Fang, Magdalena Parks & Caroline Appleby")
    style = input("Would you like to use a Python dictionary or a SQLite database? Type 'dict' or 'db': ")
    filename = input("Create an inverted index! Please input the filename: ")
    
    if style == "dict":
        try:
            index = python_index.PythonIndex(filename)
        except:
            print("File not found, please try again. ")
            return
    elif style == "db":
        index = sql_index.SQLIndex(filename)
    else:
        print("Invalid input, please enter between 'dict' and 'db'.")
        return
        
    
    stop = input("How many stop words would you like? Please enter a number: ")
    try: 
        stop_num = int(stop)
    except ValueError:
        print("Not a valid number, defaulting to 10")
        stop_num = 10 
        
    print("File Imported. Basic inverted index created. ")
    print(index.get_num_words(), " entries in dictionary.")
    print(index.get_num_postings(), " total postings.")
    print(index.get_stop_words(stop_num))

    
    nxt = input("What would you like to do next? Type\n    'q' for a  query\n    'tf' for a term frequency\n    'idf' for an inverted document frequency\n    'tf/idf' for a TF/IDF value\n    'cos' for cosine similarity\nchoice: ")
    
    if nxt == "q":
        query = input("Please type your query, using 'AND' to denote conjunction: ")
        if style == 'dict':
            opt = input("What kind of function would you like to use? Type\n    's' for using the function with set\n    'n' for normal walk through\n    'o' for optimized version with skip pointers for every step\n    '2' for optimized version with fixed skip pointers\nchoices: ")
        else:
            opt = 's'
        print(index.query(query, opt))

    elif nxt == "tf":
        term = input("Please enter the term: ")
        doc = int(input("Please enter the document ID number: "))
        # print(tfidf.tf(term, doc))
        
    
    elif nxt == "idf":
        term = input("Please enter the term: ")
        # print(tfidf.idf(term, index))
        
    
    elif nxt == "tf/idf":
        term = input("Please enter the term: ")
        doc = int(input("Please enter the document ID number: "))
        # print(tfidf.tfidf(term, doc, index))
        
    else:
        print("Invalid input, please try again") 
        

    
if __name__ == "__main__":
    main()
