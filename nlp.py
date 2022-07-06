from nltk.corpus import wordnet
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

class LanguageProcessor():
    def __init__(self):
        self.command_dict = {}
        self.eng_stops = stopwords.words("english")
    
    def strtok(self, sentence):
        return nltk.word_tokenize(sentence)


    def remove_stop_words(self, sentence):
        tokens = self.strtok(sentence)
        for word in tokens:
            if word in self.eng_stops:
                tokens.remove(word)
        return ' '.join(tokens)

    def stem(self, sentence):
        words = self.strtok(sentence)
        stemmed = [PorterStemmer().stem(w) for w in words]
        return stemmed

    def lematize(self, sentence):
        words = self.strtok(sentence)
        lemmed = [WordNetLemmatizer().lemmatize(w) for w in words]
        print(lemmed)

    def find_nouns(self, sentence):
        is_noun = lambda pos: pos[:2] == 'NN'
        words = self.strtok(sentence)
        nouns = [word for (word, pos) in nltk.pos_tag(words) if is_noun(pos)] 
        return nouns


       

if __name__ == '__main__':
    lp = LanguageProcessor()
    print(lp.remove_stop_words("what's your name"))
    print(lp.stem("it is not necessarily that stem needs to exist and have a meaning"))
    print(lp.lematize("tell me what the meaning of life is"))
    print(lp.find_nouns("tell me what the meaning of life is"))