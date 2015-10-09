import urllib2
import base64
import nltk
import collections
from nltk.tokenize import RegexpTokenizer
from nltk.stem import RegexpStemmer
import math

'''
SearchEngine object that's responsible for making query requests to and get response from Bing server.
'''
class SearchEngine:
    def __init__(self, key):
        #self.accountKey = 'KtKgk8Mo5p6/rJE0FnlmA8qKVi1F7kS3OQbxik1ZnCg'
        self.accountKey = key
        self.url = None
        self.query = None

    def search(self, query):
        bingBaseUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'
        self.url = bingBaseUrl + '%20'.join(query) + "%27&$top=10&$format=Atom"
        self.query = query

        accountKeyEnc = base64.b64encode(self.accountKey + ':' + self.accountKey)
        headers = {'Authorization': 'Basic ' + accountKeyEnc}
        req = urllib2.Request(self.url, headers = headers)
        response = urllib2.urlopen(req)
        # content = response.read()

        # #save search result
        # f = open('output.xml', 'w')
        # f.write(content)
        # f.close()
        return response

    def getKey(self):
        return self.accountKey

    def getUrl(self):
        return self.url

    def getQuery(self):
        return self.query

def empty_list():
    return [0,0,0,0,0,0,0,0,0,0]

def empty_float_list():
    return [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

# get stopwords in query
def get_stopword_in_query(query, stopwords):
    S = []
    for word in query:
        if word in stopwords:
            S.append(word)
    return S

# Expand origial query based on relevence feedback
def query_expand(documents, scores, query):
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = [ word.encode('utf-8') for word in stopwords]
    stopwords_in_query = get_stopword_in_query(query, stopwords)
    words_score = collections.defaultdict(empty_list)
    weights = collections.defaultdict(empty_float_list)
    st = RegexpStemmer('ing$|s$', min=5)
    # Add scores to each word based on their frequency
    for i in range(0, len(documents)):
        tokenizer = RegexpTokenizer('\w+|\d+')
        title_words = tokenizer.tokenize(documents[i].getTitle())
        description_words = tokenizer.tokenize(documents[i].getDescription())
        for word in title_words:
            word = word.lower()
            if word not in stopwords or word in stopwords_in_query:
                words_score[word][i] += 1.2
        for word in description_words:
            word = word.lower()
            if word not in stopwords or word in stopwords_in_query:
                words_score[word][i] += 0.8
    # compute tf-idf weight
    for word in words_score:
        df = 0
        for times in words_score[word]:
            if times > 0:
                df += 1
        for i in range(0,10):
            weights[word][i] = words_score[word][i] * math.log(10.0/df)
            
    relevence_doc = collections.defaultdict(float)
    nonrelevence_doc = collections.defaultdict(float)
    relevence_doc_num = 0

    # normalization and Rocchio Algorithm
    for i in range(0, 10):
        tmp = 0.0
        for word in weights:
            tmp += math.pow(weights[word][i],2)
        tmp = math.sqrt(tmp)
        normalized_weight = collections.defaultdict(float)
        for word in weights:
            normalized_weight[word] = weights[word][i]/tmp
        if scores[i] == 1:
            relevence_doc_num += 1
            for word in normalized_weight:
                relevence_doc[word] += normalized_weight[word]
        else:
            for word in normalized_weight:
                nonrelevence_doc[word] += normalized_weight[word]

    # use default parameters as suggested in the paper
    alpha = 1
    beta  = 0.8
    gamma = 0.15
    new_score = collections.defaultdict(float)
    for word in weights:
        new_score[word] = beta * relevence_doc[word]/relevence_doc_num - gamma * nonrelevence_doc[word]/(10-relevence_doc_num)
        if word in query:
            new_score[word] += alpha
    new_terms = []
    new_query = []
    sorted_scores = sorted(new_score.iteritems(), key=lambda x: -x[1])
    # print sorted_scores

    # pick two terms with highest score
    first_new_term = None
    for s in sorted_scores:
        if s[0] not in query:
            if len(new_terms) == 1:
                if s[1] * 1.5 < first_new_term[1]:
                    break
                else:
                    new_terms.append(s[0])
                    new_query.append(s[0])
            else:
                first_new_term = s
                new_terms.append(s[0])
                new_query.append(s[0])
        else:
            new_query.append(s[0])
        if len(new_terms) > 1:
            break

    return new_terms, new_query

    #TODO   normalize scores? stopwords? description? threshore? 
