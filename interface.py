import parser
import sys

def print_parameters(key, query, url):
    print 'Parameters:'
    print 'Client key = ' + key
    print 'Query = ' + query
    print 'URL = ' + url
    print 'Total no of results: 10'
    print 'Bing Search Results:'


def interact(result):
    total_relevant = 0
    relevant_array = []
    for ans in result:
        print '--------------------'
        print ans.getTitle()
        print ans.getDescription()
        print ans.getUrl()
        isRelevant = raw_input('relevant? (y/n) ')
        if isRelevant == 'y':
            total_relevant += 1
            relevant_array.append(1)
        else:
            relevant_array.append(0)

    return relevant_array, total_relevant / 10

def print_transcript(precision, query):
    print 'Feedback Summary'
    print 'Query: ' + query
    print 'Precision: %d' % (precision)

    if precision >= 0.9:
        print 'Desired precision reached, done'
    else:
        print 'Still below the desired precision of 0.9'
        