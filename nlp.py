from nltk.corpus import wordnet
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
import joblib
import numpy as np
import pickle

LOG_MODE = False
TRAIN_MODE = False
TEST_MODE = True

class LanguageProcessor():
    def __init__(self):
        self.command_dict = {}
        self.eng_stops = stopwords.words("english")
        self.tf_idf_vect = TfidfVectorizer(ngram_range=(1,3), min_df=0.001, max_df=0.7, analyzer='word')
    
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


    def load_question_model(self):
        posts = nltk.corpus.nps_chat.xml_posts()
        posts_text = [post.text for post in posts]
        train_text = posts_text[:int(len(posts_text)*0.8)]
        test_text = posts_text[int(len(posts_text)*0.2):]
        #Get TFIDF features
        vectorizer = self.tf_idf_vect
        X_train = vectorizer.fit_transform(train_text)
        #Get TFIDF features
        clf =  self.load_model('question.pkl')
        #print(clf.predict(vectorizer.transform(['who is michael jordan'])))
        return clf



    def train_question_detector(self):
        posts = nltk.corpus.nps_chat.xml_posts()
        posts_text = [post.text for post in posts]
        train_text = posts_text[:int(len(posts_text)*0.8)]
        test_text = posts_text[int(len(posts_text)*0.2):]

        #Get TFIDF features
        vectorizer = self.tf_idf_vect
        X_train = vectorizer.fit_transform(train_text)
        X_test = vectorizer.transform(test_text)

        y = [post.get('class') for post in posts]
        y_train = y[:int(len(posts_text)*0.8)]
        y_test = y[int(len(posts_text)*0.2):]

        # Fitting Gradient Boosting classifier to the Training set
        gb = GradientBoostingClassifier(n_estimators = 400, random_state=0) 
  
        gb.fit(X_train, y_train)
        predictions_rf = gb.predict(X_test)
        print(classification_report(y_test, predictions_rf))
        self.save_model(gb, 'question.pkl')
        return gb



    def save_model(self, clf, name):
        with open(name, 'wb') as f:
            pickle.dump(clf, f)

    def load_model(self, name):
        return joblib.load(name)

        


if __name__ == '__main__':
    lp = LanguageProcessor()
    if TRAIN_MODE:
        lp.train_question_detector()
    elif TEST_MODE:
        clf = lp.load_question_model()
        vectorizer = lp.tf_idf_vect
        print(clf.predict(vectorizer.transform(['who is michael jordan'])))


    
    if LOG_MODE:
        print(lp.remove_stop_words("what's your name"))
        print(lp.stem("it is not necessarily that stem needs to exist and have a meaning"))
        print(lp.lematize("tell me what the meaning of life is"))
        print(lp.find_nouns("tell me what the meaning of life is"))