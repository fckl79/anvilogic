#### 1. Config File - model_congfig.json
* tag = "gensim_doc2vec" - name of model
 -- model parameters in corresponding dictionary


Parameters
* train_data - _valid_ path where data are stored from scraped MITRE Att@ck site
* model_file - _valid_ path where model file will be stored after being saved
* corpus_file - _valid_ path of corpus file -- we do not use/save it any longer
* matrix_file - _valid_ path of file containing matrix of unit vectors related MITRE Att@ck documents

* Other Parameters - related to gensim.Doc2Vec model parameters
  -- n_grams
  -- min_count
  -- window
  -- epochs

#### 2. How to Get Training Data - Scraping MITRE Att@ck site
_data_scraper.groups_scraper.save_data("C:\\Users\\Igor\\Projects\\anvilogic\\test\\model_data.json")_

does it all. Parameter here is the same path as in config file for _train_data_ key.

#### 3. How to Train and Save the Model
In train_mode/train_model/gensim_doc2vec.py run
cls = GensimDoc2Vec("c:\\Users\\Igor\\Projects\\anvilogic\\test\\model_config.json",
                        "gensim_doc2vec")

cls.train()

cls.save()

It will save model and matrix file to corresponding locations in config file

#### 4. How to Run the Model
In train_mode/train_model/gensim_doc2vec.py run

cls = GensimDoc2Vec("c:\\Users\\Igor\\Projects\\anvilogic\\test\\model_config.json",
                        "gensim_doc2vec")

cls.load()
sims1 = cls.predict("Base64 encoded HTTP request")
print(sims1)
