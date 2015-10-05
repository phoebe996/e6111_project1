import urllib2
import base64
import nltk
import collections

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

# TODO
# Expand origial query based on relevence feedback
def query_expand(documents, scores, query):
    print 'documents'
    print documents
    print 'scores'
    print scores
    stopwords = nltk.corpus.stopwords.words('english')
    words_score = collections.defaultdict(int)
    top_two_words = [('',0),('',0)]
    total_score = 0
    new_terms = []
    for i in range(0, len(documents)):
        if scores[i] == 1:
            total_score += 1
            words = documents[i].getTitle().split()
            print 'current words'
            print words
            for word in words:
                if word not in stopwords:
                    words_score[word] += 1
                    if word not in query and words_score[word] > top_two_words[1][1]:
                        if words_score[word] > top_two_words[0][1]:
                            top_two_words[1] = top_two_words[0]
                            top_two_words[0] = (word, words_score[word])
                        else:
                            top_two_words[1] = (word, words_score[word])

    if top_two_words[0][1] >= total_score:
        new_terms.append(top_two_words[0][0])
    if top_two_words[1][1] >= total_score:
        new_terms.append(top_two_words[1][0])
    print words_score
    query.extend(new_terms)
    all_terms_with_score = {}
    for term in query:
        all_terms_with_score[term] = words_score[term]
    new_query = []
    for s in sorted(all_terms_with_score.iteritems(), key=lambda x: x[1]):
        new_query.insert(0,s[0])
    print all_terms_with_score
    print new_terms
    print new_query
    return new_terms, new_query
