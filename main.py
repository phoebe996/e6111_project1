import sys
import search
import parser
import interface

def main(argv):
    # Get parameters from user input
    accountKey = argv[0]
    target_precision = float(argv[1])
    query = argv[2].lower().split()
    precision = 0.0
    # create a new search engine instance
    search_engine = search.SearchEngine(accountKey)
    while True:  
        # search this query on Bing 
        xml = search_engine.search(query)
        # print out search query parameters on interminal
        interface.print_parameters(search_engine, target_precision)
        # parse the xml search results to Siteinfo objects
        result = parser.parse_xml(xml)
        # if there are less than 10 results, break and quit
        if len(result) < 10:
            break
        # interact with user and let user mark relevence of each result
        array_score, precision = interface.interact(result)
        # if precision is 0, break and quit
        if precision == 0.0:
            print 'Below desired precision, but can no longer augment the query'
            break
        interface.print_transcript(precision, query, target_precision)
        # if precision is equal or larger than target precision, break and quit
        if precision >= target_precision:
            break
        # if precision is less than target precision, expand and reoder query and search again
        else:
            new_terms, new_query = search.query_expand(result, array_score, query)
            interface.print_new_terms(new_terms)
            if new_query == query:
                break
            else:
                query = new_query


if __name__ == "__main__":
    main(sys.argv[1:])
    
