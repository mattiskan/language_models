from src.ngram_model import sentence_prob, ngram_model, tokenize
from src.smoothing import additive_smoothing
from src.corpus import Corpus
       

def main():
    corpus = Corpus(3)

    with open('lines.txt', 'r') as rfile:
        for line in rfile:
            if line:
                corpus.add_sentence(line.strip())

    while True:
        sentence = input('\n\n> ')
        print(sentence_prob(sentence, ngram_model(2, additive_smoothing), corpus))

if __name__ == '__main__':
    main()
    
