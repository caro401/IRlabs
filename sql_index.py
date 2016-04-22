import sqlite3
import math
import inverted_index


class SQLIndex(inverted_index.InvertedIndex):

    def __init__(self, frequency):

        # Open SQLite and create table
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE inverted_index
                     (word text, document int, amt text)''')

        # create indices on doc and word for efficieny.
        self.c.execute('''CREATE INDEX doc
                      ON inverted_index (document)''')
        self.c.execute('''CREATE INDEX word
                      ON inverted_index (word)''')

        with open(frequency, "r", encoding="utf8") as fobj:
            for line in fobj:
                count, word, document = line.split(" ")
                # Insert a row of data
                self.c.execute("INSERT INTO inverted_index VALUES (?, ?, ?)", (word, document, count))

        # Save (commit) the changes
        self.conn.commit()

    def get_num_words(self):
        c = self.conn.cursor()
        # subquery returns a table containing the list of unique words
        # outer query returns the number of entries in the subquery
        num_words = self.c.execute("select count(*) from (select word from inverted_index group by word) as A").fetchone()
        return num_words[0]

    def get_num_postings(self):
        c = self.conn.cursor()
        # returns the number of entries in inverted_index
        num_postings = self.c.execute("SELECT count(*) FROM inverted_index").fetchone()
        return num_postings[0]

    def get_stop_words(self, num_stop):
        c = self.conn.cursor()

        # finds all unique words in inverted_index, and the count of documents the word is found in
        # then orders the results by the count
        # then returns the first N entries
        self.c.execute('''SELECT word, count(*) as c
            from inverted_index
            GROUP BY word
            ORDER BY c DESC
            LIMIT ?''', (num_stop,))

        # add to set for returning
        ret = set()
        for entry in self.c.fetchall():
            ret.add(entry[0])

        print(self.get_num_words() - num_stop, "words in dictionary after the stop words are removed. ")

        # subquery is same as above
        # we left join it to the full set, and remove entries where inner query has values
        #   ie, we remove entries which contain words found in the subquery
        # then we return the number of rows
        self.c.execute('''SELECT count(*)
            FROM inverted_index
            LEFT JOIN (SELECT word, count(*) as c
                from inverted_index
                GROUP BY word
                ORDER BY c DESC
                LIMIT ?) as A
            ON inverted_index.word = A.word
            WHERE A.word is null
            ''', (num_stop,))

        num_postings = self.c.fetchone()
        num_postings = num_postings[0]

        print(num_postings, "total postings after the stop words are removed. ")

        return ret

    def query(self, q, opt=""):
        c = self.conn.cursor()
        words = q.split(" AND ")

        # we need to have as many question marks in the IN clause as there are words in the query
        questionmark_string = ','.join('?'*len(words))

        # we can use words as the values for the query
        # but we need to fill in the value at the end, which needs to be the total number of words
        # so we add that to the list
        words.append(len(words))

        # find all word, document pairs which have a word from the query
        # then find each unique document from those entries, as well as the number of words from the query it has, c
        # only return documents where c is the number of words in the query
        #   ie, return documents which contain ALL words
        self.c.execute('''SELECT document, count(*) as c
            from inverted_index
            where word IN (%s)
            GROUP BY document
            HAVING c = ?''' % questionmark_string, words)

        # bundle up result for returning
        ret = list()
        for entry in self.c.fetchall():
            ret.append(int(entry[0]))
        return ret

    def tf(self, term, doc):
        c = self.conn.cursor()

        # find the entry corresponding to the word and document, and return the raw frequency
        self.c.execute("select amt from inverted_index where word like ? and document=?", (term, doc))
        q_result = self.c.fetchone()
        return 1 + math.log(int(q_result[0]), 10)

    def idf(self, term):
        c = self.conn.cursor()

        # inner query finds all unique documents
        # main query counts the number of entries (documents) from the inner query
        q = self.c.execute("SELECT count(*) FROM (SELECT document from inverted_index GROUP BY document) as A")
        num_docs = q.fetchone()
        num_docs = num_docs[0]

        # idf defined as log_10 N/(df_t)
        df = len(self.query(term))
        return math.log((num_docs/df), 10)

