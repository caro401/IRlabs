import sqlite3
import math
import inverted_index


class SQLIndex(inverted_index.InvertedIndex):

    def __init__(self, frequency):

        # Open SQLite and create table
        self.conn = sqlite3.connect(":memory:")
        c = self.conn.cursor()
        c.execute('''CREATE TABLE inverted_index
                     (word text, document int, amt text)''')

        with open(frequency, "r", encoding="utf8") as fobj:
            for line in fobj:
                count, word, document = line.split(" ")
                # Insert a row of data
                c.execute("INSERT INTO inverted_index VALUES (?, ?, ?)", (word, document, count))

        # Save (commit) the changes
        self.conn.commit()

    def get_num_words(self):
        c = self.conn.cursor()
        num_words = c.execute("select count(*) from (select word from inverted_index group by word) as A").fetchone()
        return num_words[0]

    def get_num_postings(self):
        c = self.conn.cursor()
        num_postings = c.execute("SELECT count(*) FROM inverted_index").fetchone()
        return num_postings[0]

    def get_stop_words(self, num_stop):
        c = self.conn.cursor()

        c.execute("SELECT word, count(*) as c \
            from (SELECT word, document \
            from inverted_index \
            GROUP BY word, document) as A \
            GROUP BY word \
            ORDER BY c DESC \
            LIMIT ?", (num_stop,))

        ret = set()
        for entry in c.fetchall():
            ret.add(entry[0])

        print(self.get_num_words() - num_stop, "words in dictionary after the stop words are removed. ")

        c.execute("SELECT count(*) FROM inverted_index where word not in ( \
            select word from (SELECT word, count(*) as c \
                from (SELECT word, document \
                from inverted_index \
                GROUP BY word, document) as A \
                GROUP BY word \
                ORDER BY c DESC \
                LIMIT ?) as B \
            )", (num_stop,))

        num_postings = c.fetchone()
        num_postings = num_postings[0]

        print(num_postings, "total postings after the stop words are removed. ")

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

    def tf(self, term, doc):
        c = self.conn.cursor()
        c.execute("select amt from inverted_index where word like ? and document=?", (term, doc))
        q_result = c.fetchone()
        return 1 + math.log(int(q_result[0]), 10)

    def idf(self, term):
        c = self.conn.cursor()
        q = c.execute("SELECT count(*) FROM (SELECT document from inverted_index GROUP BY document) as A")
        num_docs = q.fetchone()
        num_docs = num_docs[0]

        # idf defined as log_10 N/(df_t)
        df = len(self.query(term))
        return math.log((num_docs/df), 10)

