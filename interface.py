import parser
import sys

def print_parameters(key, query, url):
    print 'Parameters:'
    print 'Client key = ' + key
    print 'Query = ' + query
    print 'URL = ' + url
    print 'Total no of results: 10'
    print 'Bing Search Results:'
    print '======================'


def interact(result):
    total_relevant = 0
    relevant_array = []
    N = 1
    for ans in result:
        print 'Result %d' % (N)
        print '['
        print ' Title: ' + ans.getTitle()
        print ' Summary: ' + ans.getDescription()
        print ' URL ' + ans.getUrl()
        print ']'

        isRelevant = raw_input('Relevant (Y/N)? ')
        if isRelevant.lower() == 'y':
            total_relevant += 1
            relevant_array.append(1)
        else:
            relevant_array.append(0)
        N = N + 1

    print total_relevant, N-1

    return relevant_array, total_relevant / 10.0

def print_transcript(precision, query):
    print '======================'
    print 'Feedback Summary'
    print 'Query: ' + query
    print 'Precision: %.1f' % (precision)

    if precision >= 0.9:
        print 'Desired precision reached, done'
    else:
        print 'Still below the desired precision of 0.9'
        