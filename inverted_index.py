import tfidf_util


class InvertedIndex:
    # Abstract class InvertedIndex for reuse of tfidf code

    def get_num_words(self):
        raise NotImplementedError("Abstract class InvertedIndex does not implement get_num_words()")

    def get_num_postings(self):
        raise NotImplementedError("Abstract class InvertedIndex does not implement get_num_postings()")

    def get_stop_words(self):
        raise NotImplementedError("Abstract class InvertedIndex does not implement get_stop_words()")

    def tf(self, term, doc_id):
        raise NotImplementedError("Abstract class InvertedIndex does not implement tf(term, doc_id)")

    def idf(self, term):
        raise NotImplementedError("Abstract class InvertedIndex does not implement idf(term)")

    def query(self, query_str):
        '''
        Finds all documents containing every given term
        :param query_str: a string containing a list of terms separated by 'AND'
            For example, 'kids AND really AND school'
        :return: a list of document ids
        '''
        raise NotImplementedError("Abstract class InvertedIndex does not implement query(query_str)")

    def tfidf(self, term, doc_id):
        # calculate the tf/idf
        # using the definition given in the lecture slides
        tf = self.tf(term, doc_id)
        idf = self.idf(term)
        return tf*idf

    def compute_sim(self, query_str):
        # find all the docs matching query, assumiung this will be lowercased already
        doc_list = self.query(query_str)

        # compute vector of tf/idf for query terms
        query_terms = query_str.split(" AND ")
        query_vector = []  # compute tf/idf for each term in query wrt query in here
        # going to assume unique query terms, so raw tf = 1, scaled tf = 1 + log_10(1) = 1
        for term in query_terms:
            query_vector.append(self.idf(term))
        print(query_vector)

        scores = []  # this will be a list of tuples (doc-id, cosine-sim)

        # compute vector of tf/idf weights for each document, then calculate cosine similarity between document and query vectors
        for doc in doc_list:
            doc_vector = []
            for term in query_terms:
                doc_vector.append(self.tfidf(term, doc)) # compute vector of tf/idf of all query
            sim = tfidf_util.cosine_sim(query_vector, doc_vector) # compute cosine_sim of that vector with the query vector
            print("Sim:",doc_vector,sim)
            scores.append((doc, sim))

        print(scores)
        # rank docs according to similarity
        scores = sorted(scores, key=lambda x: x[1])  # sort the list of tuples on the cosine sim
        #TODO check this comes out in the right order!

        # return ordered list of docs
        ordered_docs =  [x[0] for x in scores]  # I hope this will give you a list consisting just of the first bit of each tuple, ie the docID
        return ordered_docs


