import parser
import sys

def print_parameters(search_engine, precision):
    print 'Parameters:'
    print 'Client key  = ' + search_engine.getKey()
    print 'Query       = ' + ' '.join(search_engine.getQuery())
    print 'Precision   = ' + str(precision)
    print 'URL: ' + search_engine.getUrl()
    print 'Total no of results: 10'
    print 'Bing Search Results:'
    print '======================'


def interact(result):
    total_relevant = 0
    array_score = []
    N = 1
    for ans in result:
        print 'Result %d' % (N)
        print '['
        print ' URL: ' + ans.getUrl()
        print ' Title: ' + ans.getTitle()
        print ' Summary: ' + ans.getDescription()
        print ']\n'

        isRelevant = raw_input('Relevant (Y/N)? ')
        if isRelevant.lower() == 'y':
            total_relevant += 1
            array_score.append(1)
        else:
            array_score.append(0)
        N = N + 1
    return array_score, total_relevant / 10.0

def print_transcript(precision, query, target_precision):
    print '======================'
    print 'FEEDBACK SUMMARY'
    print 'Query: ' + ' '.join(query)
    print 'Precision: %.1f' % (precision)

    if precision >= target_precision:
        print 'Desired precision reached, done'
    else:
        print 'Still below the desired precision of ' + str(target_precision)
    
def print_new_terms(new_terms):
    print 'Indexing results ....'
    print 'Indexing results ....'
    print 'Augmenting by ' + ' '.join(new_terms)
    if len(new_terms) == 0:
        print 'Below desired precision, but can no longer augment the query'