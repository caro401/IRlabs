import sqlite3

class SQLIndex:

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

    def get_num_words(self):
        c = self.conn.cursor()
        num_words = c.execute("SELECT count(*) FROM inverted_index GROUP BY word").fetchone()
        return num_words[0]

    def get_num_postings(self):
        c = self.conn.cursor()
        num_postings = c.execute("SELECT count(*) FROM inverted_index").fetchone()
        return num_postings[0]

    def get_stop_words(self, num_stop):
        c = self.conn.cursor()

        c.execute("SELECT word, count(*) as c \
        from inverted_index \
        GROUP BY word \
        ORDER BY c DESC \
        LIMIT ?", (num_stop,))

        print("Stopwords: ")
        print(c.fetchall())

    def query(self, q):
        c = self.conn.cursor()

        words = q.replace(" AND ", ", ")
        c.execute("SELECT document from inverted_index where word IN(?) GROUP BY document", (words,))

        print(c.fetchall())



