import timeit

def analyze(words, iterations=1000):
    setup = '''
import python_index, sql_index
py = python_index.PythonIndex("index_lc_tf.txt")
sql = sql_index.SQLIndex("index_lc_tf.txt")
    '''

    query = " AND ".join(words)

    s = min(timeit.Timer('py.query("'+query+'","s")', setup=setup).repeat(1, iterations))
    n = min(timeit.Timer('py.inter_queries_re("'+query+'")', setup=setup).repeat(1, iterations))
    o = min(timeit.Timer('py.inter_queries_op("'+query+'")', setup=setup).repeat(1, iterations))
    o2 = min(timeit.Timer('py.inter_queries_op_2("'+query+'")', setup=setup).repeat(1, iterations))
    sql = min(timeit.Timer('sql.query("'+query+'")', setup=setup).repeat(1, iterations))

    py_cos = min(timeit.Timer('py.query("'+query+'")', setup=setup).repeat(1, iterations))
    sql_cos = min(timeit.Timer('sql.compute_sim("'+query+'")', setup=setup).repeat(1, iterations))

    print(len(words), round(s,4), round(n,4), round(o,4), round(o2,4), round(py_cos,4), "|", round(sql,4), round(sql_cos,4))

print("Infrequent words")
words = ["doubled", "$250", "ain'", "links", "suzi", "grown", "deeply", "growls", "spiders", "complex"]
for i in range(1, len(words)+1):
    analyze(words[:i])


print()
print("Frequent words")
words = [".", ",", "you", "?", "i", "the", "to", "s", "a", "-"]
for i in range(1, len(words)+1):
    analyze(words[:i])


print()
print("Random words")
words = ["all", "it'", "then", "mrs.", "for", "re", "gift", "day", "to", "were"]
for i in range(1, len(words)+1):
    analyze(words[:i])



