import os

from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import json
import re
import nltk
import pickle

from nltk.corpus import stopwords as stopwords_corpus
from nltk.tokenize import word_tokenize
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')


def convert_slang(sentence, slang_dict):
    words = word_tokenize(sentence)
    normalized_words = []
    for word in words:
        if word in slang_dict:
            normalized_words.append(slang_dict[word])
        else:
            normalized_words.append(word)
    
    sentence = " ".join(normalized_words)
    
    return sentence

def remove_stopwords(sentence, stopwords):
    words = word_tokenize(sentence)
    filtered_words = []
    for word in words:
        if word not in stopwords:
            filtered_words.append(word)

    sentence = " ".join(filtered_words)
    return sentence

def get_text(message):
    """
    mendapatkan hasil praproses text
    """
    django_path = os.path.abspath(os.path.dirname(__name__)) + '\ml-model'

    with open(django_path + '\combined_slang_words.txt','r') as file:
        slang_dict=json.loads(file.read())

    slang_dict.update({'plg':'pelanggan',
                    'yth':'yang terhormat',
                    'rb':'ribu',
                    'rp':'rupiah',
                    })

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    stopwords = stopwords_corpus.words('indonesian')
    stopwords.append(open(django_path + '\combined_stop_words.txt','r').read().split('\n'))

    data = message.lower()
    data = re.sub('http\S+|www.\S+|tsel.me\S+', '', data)
    data = re.sub('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s*', '', data)
    data = re.sub('[^a-zA-Z ]+', '', data)
    data = convert_slang(data, slang_dict)
    data = stemmer.stem(data)
    data = remove_stopwords(data, stopwords)

    with open(django_path + '/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    word_seq_train = tokenizer.texts_to_sequences([data])

    #pad sequences
    data_input = sequence.pad_sequences(word_seq_train, maxlen=65)

    return data_input