import sqlite3

class SQLVersion:
    
    def __init__(self, filename):
    
        # Open SQLite and create table
        self.conn = sqlite3.connect(":memory:")
        c = self.conn.cursor()
        c.execute('''CREATE TABLE inverted_index
                     (word text, document text)''')
        
        with open(filename, "r", encoding="utf8") as fobj:
            for line in fobj:
                word, document = line.split()
                # Insert a row of data
                c.execute("INSERT INTO inverted_index VALUES (?, ?)", (word, document))
        
        # Save (commit) the changes
        self.conn.commit()
        print("File Imported. ")
    
        num_words = c.execute("SELECT count(*) FROM inverted_index GROUP BY word").fetchone()
        num_words = num_words[0]
        num_postings = c.execute("SELECT count(*) FROM inverted_index").fetchone()
        num_postings = num_postings[0]
        print(num_words, " entries in dictionary.")
        print(num_postings, " total postings.")
        
        
    def get_stop_words(self, num_stop):
        c = self.conn.cursor()
        
        c.execute("SELECT word, count(*) as c \
        from inverted_index \
        GROUP BY word \
        ORDER BY c DESC \
        LIMIT 10")
        
        print("Stopwords: ")
        print(c.fetchall())
        
        query = input("Query: ")
        words = query.replace(" AND ",", ")
        
        c.execute("SELECT document from inverted_index where word IN(?) GROUP BY document",(words,))
        
        print(c.fetchall())
        
    
    def generate_term_freq_file(self, filename):
        c = self.conn.cursor()
        with open(filename,"w", encoding="utf8") as fobj:
            c.execute("SELECT count(*) as freq, word, document \
            FROM inverted_index GROUP BY word, document")
            
            print(c.fetchall())
            
    
