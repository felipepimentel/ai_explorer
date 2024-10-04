from gensim import corpora
from gensim.models import LdaMulticore
from gensim.parsing.preprocessing import STOPWORDS
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')

class TopicDetector:
    def __init__(self, num_topics=10):
        self.num_topics = num_topics
        self.dictionary = None
        self.lda_model = None

    def preprocess(self, text):
        return [word.lower() for word in word_tokenize(text) if word.lower() not in STOPWORDS]

    def fit(self, documents):
        preprocessed_docs = [self.preprocess(doc) for doc in documents]
        self.dictionary = corpora.Dictionary(preprocessed_docs)
        corpus = [self.dictionary.doc2bow(doc) for doc in preprocessed_docs]
        self.lda_model = LdaMulticore(corpus=corpus, id2word=self.dictionary, num_topics=self.num_topics)

    def detect_topics(self, text):
        bow = self.dictionary.doc2bow(self.preprocess(text))
        return self.lda_model.get_document_topics(bow)

# Uso:
# detector = TopicDetector(num_topics=5)
# detector.fit(["Document 1 text", "Document 2 text", ...])
# topics = detector.detect_topics("New document text")