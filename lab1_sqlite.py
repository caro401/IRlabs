import sqlite3

# Open SQLite and create table
conn = sqlite3.connect(":memory:")
c = conn.cursor()
c.execute('''CREATE TABLE inverted_index
             (word text, document text)''')

filename = input("Please input the filename: ")
with open(filename, "r", encoding="utf8") as fobj:
    for line in fobj:
        word, document = line.split()
        # Insert a row of data
        c.execute("INSERT INTO inverted_index VALUES (?, ?)", (word, document))

# Save (commit) the changes
conn.commit()
print("File Imported. ")

# # TODO: Print out number of entries
# num_words = c.execute("")
# num_postings = c.execute("")
# print(num_words, " entries in dictionary.")
# print(num_postings, " total postings.")

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

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
