""" ref: http://joneschen.org/spigdog/papers/h015a-techreport.pdf """

DEBUG = True

def no_smoothing(ngram, corpus):
    if DEBUG:
        print(ngram, corpus.count(ngram))
        print(ngram[:-1] + ('*',), corpus.count(ngram[:-1]))
        print('|V|', corpus.total(1))
        print('p:',  corpus.count(ngram) / float(corpus.count(ngram[:-1])))
        print()
    
    return corpus.count(ngram) / float(corpus.count(ngram[:-1]))

def add_one_smoothing(ngram, corpus, delta=1):
    numerator = delta + corpus.count(ngram)
    denominator = delta*corpus.total(1) + corpus.count(ngram[:-1])

    if DEBUG:
        print(ngram, corpus.count(ngram))
        print(ngram[:-1] + ('*',), corpus.count(ngram[:-1]))
        print('|V|', corpus.total(1))
        print('p:',  numerator / float(denominator))
        print()

    return numerator / float(denominator)
