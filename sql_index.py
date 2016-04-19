import sqlite3
import math
import tfidf_util

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

        ret = set()
        for entry in c.fetchall():
            ret.add(entry[0])
        return ret

    def query(self, q, opt=""):
        c = self.conn.cursor()
        words = q.split(" AND ")
        words.append(len(words))

        c.execute("SELECT document, count(*) as c from inverted_index \
            where word IN (%s) \
            GROUP BY document \
            HAVING c = ?" % ','.join('?'*(len(words)-1)), words)

        ret = list()
        for entry in c.fetchall():
            ret.append(int(entry[0]))
        return ret

    def idf(self, term):
        c = self.conn.cursor()
        q = c.execute("SELECT count(*) FROM (SELECT document from inverted_index GROUP BY document) as A")
        num_docs = q.fetchone()
        num_docs = num_docs[0]

        # idf defined as log_10 N/(df_t)
        df = len(self.query(term))
        return math.log((num_docs/df), 10)

    def tfidf(self, term, doc, filename):
        # calculate the tf/idf
        # using the definition given in the lecture slides
        tf = tfidf_util.tf(term, doc, filename)
        idf = self.idf(term)
        return tf*idf

    def compute_sim(self, query_str):  # TODO!
        # find all the docs matching query, assumiung this will be lowercased alread
        doc_list = self.query(query_str)
        # compute vector of tf/idf for query terms
        query_terms = query_str.split(" AND ")
        query_vector = []  # compute tf/idf for each term in query wrt query in here
        # going to assume unique query terms, so raw tf = 1, scaled tf = 1 + log_10(1) = 1
        for term in query_terms:
            query_vector.append(self.idf(term))

        scores = []  # this will be a list of tuples (doc-id, cosine-sim)

        for doc in doc_list:
            doc_vector = []
            for term in query_terms:
                doc_vector.append(self.tfidf(doc, term)) # compute vector of tf/idf of all query
            sim = tfidf_util.cosine_sim(query_vector, doc_vector) # compute cosine_sim of that vector with the query vector
            scores.append((doc, sim))

                # rank docs according to similarity

        scores = sorted(scores, key=lambda x: x[1])  # sort the list of tuples on the cosine sim


        # return ordered list of docs
        ordered_docs =  [x[0] for x in scores]  # I hope this will give you a list consisting just of the first bit of each tuple, ie the docID
        return ordered_docs



