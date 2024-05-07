import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from num2words import num2words
import re

def get_wordnet_pos(tag_parameter):

    tag = tag_parameter[0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    
    return tag_dict.get(tag, wordnet.NOUN)

def extract_all_sections(s):
    numeric_sections = re.findall(r'\d+', s)  # Extracting all numeric sections
    alpha_sections = re.findall(r'[a-zA-Z]+', s)  # Extracting all alphabetic sections
    return numeric_sections, alpha_sections


def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-–…°./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', ' ')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", " ")

def stemming(data):
    stemmer= PorterStemmer()
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def lemmatization(data):
    # Tokenize into words
    words = word_tokenize(str(data))
    # POS tagging
    pos_tags = pos_tag(words)
    lemmatizer = WordNetLemmatizer()
    new_text = ""
    for word, tag in pos_tags:
        new_text = new_text + " " + lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag))
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def correct_sentence_spelling(data) :
    spell = SpellChecker()
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        corrected = spell.correction(w)
        if corrected is None:
            corrected =  w
        new_text = new_text + " " + corrected
    return new_text

def alpha_num_separator(data):
    words = word_tokenize(str(data))
    new_word=' '
    for word in words:
        numeric_sections, alpha_sections = extract_all_sections(word)
        for section in numeric_sections:
            new_word+=section+' '
        for section in alpha_sections:
            new_word+=section+' '
    return new_word

def preprocess(data):
    old_data=data
    data = convert_lower_case(data)
    data = alpha_num_separator(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    # data = correct_sentence_spelling(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = correct_sentence_spelling(data)
    # data = stemming(data)
    data = lemmatization(data)
    # data = remove_punctuation(data)
    # data = convert_numbers(data)
    # data = stemming(data) #needed again as we need to stem the words
    # # data = lemmatization(data)
    # data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    # return old_data if data == '' else data
    return data