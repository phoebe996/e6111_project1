import urllib2
import base64

class SearchEngine:
    def __init__(self):
        self.accountKey = 'KtKgk8Mo5p6/rJE0FnlmA8qKVi1F7kS3OQbxik1ZnCg'
        self.url = None
        self.query = None

    def search(self, query):
        bingBaseUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'
        self.url = bingBaseUrl + query + "%27&$top=10&$format=Atom"
        print 'URL: ' + self.url
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
    
