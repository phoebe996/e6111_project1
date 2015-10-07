import urllib2
import base64
import nltk
import collections
from nltk.tokenize import RegexpTokenizer
import math

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
# TODO
# Expand origial query based on relevence feedback
def query_expand(documents, scores, query):
    stopwords = nltk.corpus.stopwords.words('english')
    words_score = collections.defaultdict(empty_list)
    weights = collections.defaultdict(empty_float_list)
    for i in range(0, len(documents)):
        tokenizer = RegexpTokenizer('\w+|\d+')
        words = tokenizer.tokenize(documents[i].getTitle())
        #words = tokenizer.tokenize(documents[i])
        for word in words:
            if word not in stopwords:
                word = word.lower()
                words_score[word][i] += 1
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
    print relevence_doc
    print nonrelevence_doc
    new_score = collections.defaultdict(float)
    for word in weights:
        new_score[word] = 0.8 * relevence_doc[word]/relevence_doc_num - 0.1 * nonrelevence_doc[word]/(10-relevence_doc_num)
        if word in query:
            new_score[word] += 1
    new_terms = []
    new_query = []
    sorted_scores = sorted(new_score.iteritems(), key=lambda x: -x[1])
    print sorted_scores
    for s in sorted_scores:
        if s[1] >= 0.1:
            new_query.append(s[0])
            if s[0] not in query:
                new_terms.append(s[0])
            if len(new_terms) >= 2:
                break
        else:
            break
    return new_terms, new_query

if __name__=='__main__':
    query_expand([
        'Hello New York city hello.',
        'hello',
        'hello new york', 
        'hello seattle', 
        'seattle is raining again', 
        'hello again new york', 
        'new york city rocks', 
        'columbia university in the city of new york',
        'winter is coming in new york',
        'winter is coming'
        ], 
        [1,0,1,0,0,1,1,1,1,0],['new', 'york'])
    #TODO   normalize scores? stopwords? description? threshore? 