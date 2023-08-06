import importlib
from kolibri.datasets.ag_news import Ag_news
from kolibri.datasets.amazonreviews import AmazonReviews
from kolibri.datasets.amazonreviewsentiments import AmazonReviewSentiments
from kolibri.datasets.conll2000 import CoNLL2000
from kolibri.datasets.dbpedia import DBpedia
from kolibri.datasets.enwik9 import EnWik9
from kolibri.datasets.imdb import Imdb
from kolibri.datasets.iwslt2016 import Iwslt2016
from kolibri.datasets.iwslt2017 import Iwslt2017
from kolibri.datasets.penntreebank import PennTreebank
from kolibri.datasets.sogounews import SogouNews
from kolibri.datasets.squad1 import SQuAD1
from kolibri.datasets.squad2 import SQuAD2
from kolibri.datasets.udpos import Udpos
from kolibri.datasets.wikitext103 import WikiText103
from kolibri.datasets.wikitext2 import WikiText2
from kolibri.datasets.yahooanswers import YahooAnswers
from kolibri.datasets.yelpreviews import YelpReviews
from kolibri.datasets.yelpreviewsentiments import YelpReviewSentiments
from kolibri.datasets.multi30k import Multi30k
from kolibri.datasets.conll2003 import CoNLL2003
from kolibri.datasets.sentiment140 import Sentiment140
from kolibri.datasets.creditcardfraud import CreditCardFraud
from kolibri.datasets.consumercomplaints import ConsumerComplaints
from kolibri.datasets.snipsintents import SnipsIntents

DATASETS = {
    'AG_NEWS': Ag_news,
    'AmazonReviews': AmazonReviews,
    'AmazonReviewSentiments': AmazonReviewSentiments,
    'CoNLL2000': CoNLL2000,
    'DBpedia': DBpedia,
    'EnWik9': EnWik9,
    'Imdb': Imdb,
    'Iwslt2016': Iwslt2016,
    'Iwslt2017': Iwslt2017,
    'PennTreebank': PennTreebank,
    'SQuAD1': SQuAD1,
    'SQuAD2': SQuAD2,
    'SogouNews': SogouNews,
    'UDPOS': Udpos,
    'WikiText103': WikiText103,
    'WikiText2': WikiText2,
    'YahooAnswers': YahooAnswers,
    'YelpReviews': YelpReviews,
    'YelpReviewSentiments': YelpReviewSentiments,
    'Multi30k': Multi30k,
    'CoNLL2003': CoNLL2003,
    'Sentiment140': Sentiment140,
    'CreditCardFraud': CreditCardFraud,
    'ConsumerComplaints': ConsumerComplaints,
    'SnipsIntents': SnipsIntents
}

URLS = {}
NUM_LINES = {}
MD5 = {}
for dataset in DATASETS:
    dataset_module_path = "kolibri.datasets." + dataset.lower()
    dataset_module = importlib.import_module(dataset_module_path)
    URLS[dataset] = dataset_module.URL
    NUM_LINES[dataset] = dataset_module.NUM_LINES
    MD5[dataset] = dataset_module.MD5

__all__ = sorted(list(map(str, DATASETS.keys())))
