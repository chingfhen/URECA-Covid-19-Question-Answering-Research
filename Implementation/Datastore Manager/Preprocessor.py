import re 
import copy
import random

# purpose: removes urls, excess spaces and newlines etc.
# input: str
# output: str
def cleanText(text):                                       
    def remove_links(text):
        return re.sub(r'http\S+', '', text)                    
    def white_space_fix(text):
        return ' '.join(text.split())
    def remove_escape_sequence_char(text):
        return text.replace(u'\xa0', u'').replace('\n', '').replace('\t', '').replace('\r', '')
    return white_space_fix(remove_escape_sequence_char(remove_links(text)))


# purpose: converts text into haystack document format
# input: str
# output: dict - {'text':...,'meta':{'name':...,'category':...}}
def text2HaystackFormat(text, name = None, category = None):
    return {'text':text, 'meta':{'name':name, 'category': category}}


# purpose: splits squad json data into train and test
# input: json
# output: train json, test json
def train_test_split(data,validation_fraction = 0.3):
    random.shuffle(data['data'])
    return {'data':data['data'][int(validation_fraction*len(data['data'])):]},{'data':data['data'][:int(validation_fraction*len(data['data']))]}

