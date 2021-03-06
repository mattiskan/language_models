import src.datasets


from nltk.corpus import brown
from src.ngram_model import sentence_prob, ngram_model, tokenize
from src.smoothing import kneser_ney
       

def main():
    while True:
        sentence = input('\n> ').split()
        print(sentence_prob(sentence, ngram_model(3, kneser_ney), src.datasets.donald_speech(n=3)))

if __name__ == '__main__':
    main()
    
