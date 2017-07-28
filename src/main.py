from nltk.corpus import brown
from src.ngram_model import sentence_prob, ngram_model, tokenize
from src.smoothing import kneser_ney

from src.datasets import the_donald
       

def main():
    while True:
        sentence = input('\n> ')
        print(sentence_prob(sentence, ngram_model(3, kneser_ney), the_donald(n=3)))

if __name__ == '__main__':
    main()
    
