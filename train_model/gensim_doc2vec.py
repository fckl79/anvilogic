from train_model.model import Model
import json
import data_process.gensim_doc2vec as proc_file
from os import path
import pickle
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd, numpy as np
import re



def train_from_data_file(train_data_file, config):
    try:
        n_grams = int(config['n_grams'])
    except:
        n_grams = 1
    data = json.load(open(train_data_file, "r"))
    corpus = []
    for id1, text in data.items():
        rec = proc_file.process_document(text, n_grams=n_grams)
        corpus.append(TaggedDocument(rec, tags=id1))
    return train_from_corpus(corpus, config)


def train_from_corpus(corp, config, corpus_file=None):
    corpus = corp
    if corp is None:
        corpus = pickle.load(open(corpus_file, "rb"))
    try:
        min_count = int(config['min_count'])
    except:
        min_count = 10
    try:
        epochs = int(config['epochs'])
    except:
        epochs = 40
    try:
        vector_size = int(config['vector_size'])
    except:
        vector_size = 100
    try:
        window = int(config['window'])
    except:
        window = 3
    model = Doc2Vec(min_count=min_count, epochs=epochs, vector_size=vector_size, window=window)
    model.build_vocab(corpus)
    model.train(corpus, total_examples=model.corpus_count, epochs=epochs)
    return model, corpus


def extract_matrix_from_corpus(corpus, model):
    res = []
    tags = []
    for doc in corpus:
        vec = model.infer_vector(doc[0])
        nrm = np.linalg.norm(vec)
        if nrm > 0:
            vec = vec / nrm
        res.append(vec)
        tag = doc[1]
        tags.append(tag)
    df = pd.DataFrame(res)
    df.index = tags
    return df


class GensimDoc2Vec(Model):
    def __init__(self, config_file, tag):
        with open(config_file, "r") as f:
            config = json.load(f)
        self.config = config[tag]
        self.model = None
        self.corpus_file = ""
        self.train_data = None
        self.matrix = None

    def load(self):
        try:
            model_file = self.config['model_file']
        except:
            model_file = ""
        if path.exists(model_file):
            self.model = Doc2Vec.load(model_file)
            self.matrix = pd.read_csv(self.config['matrix_file'], index_col=0)
            self.train_data = json.load(open(self.config['train_data'], 'r'))

    def save(self):
        self.model.save(self.config['model_file'])
        self.matrix.to_csv(self.config['matrix_file'])

    def train(self):
        try:
            corpus_file = self.config['corpus_file']
        except:
            corpus_file = ""
        try:
            train_data_file = self.config['train_data']
        except:
            return
        self.corpus_file = corpus_file
        if path.exists(self.corpus_file):
            self.model, corpus = train_from_corpus(self.corpus_file, self.config)
            self.matrix = extract_matrix_from_corpus(corpus, self.model)
            self.train_data = json.load(open(train_data_file, "r"))
            return
        self.model, corpus = train_from_data_file(train_data_file, self.config)
        self.matrix = extract_matrix_from_corpus(corpus, self.model)
        self.train_data = json.load(open(train_data_file, "r"))

    def predict(self, text, n_top=10, th=0.9):
        try:
            n_grams = int(self.config['n_grams'])
        except:
            n_grams = 1
        words = proc_file.process_document(text, n_grams)
        vec = self.model.infer_vector(words)
        nrm = np.linalg.norm(vec)
        if nrm > 0:
            vec = vec/nrm
        mat = self.matrix
        sims = pd.Series(np.matmul(mat, vec))
        sims.sort_values(ascending=False, inplace=True)
        for i in range(n_top):
            if sims[i] >= th:
                str1 = re.sub("([^/]+)(.*)", "\\1", sims.index[i])
                simil = sims[i]
                explain = self.train_data[sims.index[i]]
                print(f"{str1} - {simil}: {explain}")
        return 0
if __name__ == "__main__":
    cls = GensimDoc2Vec("c:\\Users\\Igor\\Projects\\anvilogic\\test\\model_config.json",
                        "gensim_doc2vec")
    cls.train()
    cls.save()
    #cls.load()
    #sims1 = cls.predict("Base64 encoded HTTP request")
    #print(sims1)

