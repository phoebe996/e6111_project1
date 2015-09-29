import urllib2
import base64

def search_engine(key):
    bingBaseUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'
    URL = bingBaseUrl + key + "%27&$top=10&$format=Atom"
    print 'URL: ' + URL
    #Provide your account key here
    accountKey = 'KtKgk8Mo5p6/rJE0FnlmA8qKVi1F7kS3OQbxik1ZnCg'

    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(URL, headers = headers)
    response = urllib2.urlopen(req)
    # content = response.read()

    # #save search result
    # f = open('output.xml', 'w')
    # f.write(content)
    # f.close()

    return response
