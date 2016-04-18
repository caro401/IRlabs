import math

def dot_prod(v1, v2):
    # calculate the dot product of 2 vectors, represented as arrays
    if len(v1) != len(v2):
        print("Dot product undefined over vectors of different dimensions")
        return None
    total = 0
    for i in range(len(v1)):
        total += v1[i] * v2[i]
    return total


def cosine_sim(v1, v2):
    # compute the cosine similarity of 2 vectors
    sim = dot_prod(v1, v2) / (math.sqrt(dot_prod(v1, v1)) * math.sqrt(dot_prod(v2, v2)))  # this works because (v1.v1) = v1^2
    return sim


def tf(term, doc, filename):
        # work out the frequency of the given term in the given document
        # assume existence of doc tf_lc.txt, as made in section 3 of task
        # columns: freq, term, doc, separated by spaces? check this, and test
        with open(filename, "r", encoding="utf8") as fobj:
            for line in fobj:
                frequency, t, d = line.split()
                if term == t and int(d) == doc:
                    return 1 + math.log(int(frequency), 10)
        return 0
