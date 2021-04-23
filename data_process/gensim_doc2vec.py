import nltk
from nltk.corpus import stopwords
from nltk import ngrams
from nltk.tokenize import sent_tokenize
from nltk import WordNetLemmatizer, PorterStemmer
import re

stop_words = stopwords.words("english")
w_lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


def clean_text(text):
    text = re.sub("[,\\.]", "", re.sub("\[\\d+\]", "", text))
    return text


def get_ngrams(words, n):
    ngrams1 = ngrams(words, n)
    return [" ".join(grams) for grams in ngrams1]


def process_document(text, tag="0", n_grams=1):
    res = []
    text = clean_text(text)
    words = []
    for sent in sent_tokenize(text):
        for word in re.split("\\s+", sent):
            word = word.lower()
            if word not in stop_words:
                word = w_lemmatizer.lemmatize(word)
                word = stemmer.stem(word)
                words.append(word)
    if len(words) > 0:
        for n in range(1, n_grams + 1):
            res.extend(get_ngrams(words, n))
    return res

if __name__ == "__main__":
    res1 = process_document('@admin@338 actors used the following command following exploitation of a machine with LOWBALL malware to display network connections: netstat -ano >> %temp%\\download[1]', n_grams=3)
    print(res1)

