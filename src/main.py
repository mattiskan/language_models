from nltk.corpus import brown
from src.ngram_model import sentence_prob, ngram_model, tokenize
from src.smoothing import kneser_ney
from src.corpus import Corpus
       

def main():
    brown_dataset = (' '.join(sent) for sent in brown.sents())
    corpus = Corpus.from_dataset(2, brown_dataset)

    while True:
        sentence = input('\n> ')
        print(sentence_prob(sentence, ngram_model(2, kneser_ney), corpus))

if __name__ == '__main__':
    main()
    
