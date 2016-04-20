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


