# this is the main file, run this to call all the functions you wrote elsewhere
#TODO error handling zzzzz
import python_index, sql_index


def main():
    print("Code for Information Retrieval Lab 1 by Chiao-ting Fang, Magdalena Parks & Caroline Appleby")
    style = None
    while style != 'dict' and style != 'db':
        style = input("Would you like to use a Python dictionary or a SQLite database? Type 'dict' or 'db': ")
    index = None
    while index is None:
        filename = input("Create an inverted index! Please input the filename: ")

        if style == "dict":
            try:
                index = python_index.PythonIndex(filename)
            except:
                print("File not found, please try again. ")
                continue
        elif style == "db":
            try:
                index = sql_index.SQLIndex(filename)
            except:
                print("File not found, please try again. ")
                continue
        print("File Imported. Basic inverted index created. ")
        print(index.get_num_words(), "words in dictionary.")
        print(index.get_num_postings(), "total postings.")

    stop = input("How many stop words would you like? Please enter a number: ")
    try: 
        stop_num = int(stop)
    except ValueError:
        print("Not a valid number, defaulting to 10")
        stop_num = 10

    print("Stop Words:")
    print(index.get_stop_words(stop_num))

    nxt = None
    while nxt is None:
        nxt = input("What would you like to do next? Type\n    'q' for a  query\n    'tf' for a term frequency\n    'idf' for an inverted document frequency\n    'tf/idf' for a TF/IDF value\n    'cos' for cosine similarity (ranked search)\nchoice: \n")

        if nxt == "q":
            query = input("Please type your query, using 'AND' to denote conjunction: ")
            if query.count(" AND ") == 1 and style == 'dict':
                opt = input("What kind of function would you like to use? Type\n    's' for using the function with set (no step count)\n    'n' for normal walk through\n    'o' for optimized version with skip pointers for every step\n    '2' for optimized version with fixed skip pointers\nchoices: \n")
            else:
                opt = 's'
            print(index.query(query, opt))

        elif nxt == "tf":
            term = input("Please enter the term: ")
            doc = int(input("Please enter the document ID number: "))
            print("The given term is found in the given document", index.tf(term, doc), "time(s)")

        elif nxt == "idf":
            term = input("Please enter the term: ")
            print(index.idf(term))

        elif nxt == "tf/idf":
            term = input("Please enter the term: ")
            doc = int(input("Please enter the document ID number: "))
            print(index.tfidf(term, doc))

        elif nxt == "cos":
            term = input("Please enter the query: ")
            print(index.compute_sim(term))

        else:
            print("Invalid input, please try again")

        nxt = None
        

    
if __name__ == "__main__":
    main()
