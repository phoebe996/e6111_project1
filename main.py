import sys
import search
import parser
import interface

def main(argv):
    accountKey = argv[0]
    target_precision = float(argv[1])
    query = [word.lower() for word in argv[2:]]
    precision = 0.0
    search_engine = search.SearchEngine(accountKey)
    while True:  
        xml = search_engine.search(query)
        interface.print_parameters(search_engine, target_precision)
        result = parser.parse_xml(xml) 
        array_score, precision = interface.interact(result)
        if precision == 0.0:
            print 'Below desired precision, but can no longer augment the query'
            break
        interface.print_transcript(precision, query, target_precision)
        if precision >= target_precision:
            break
        else:
            new_terms, new_query = search.query_expand(result, array_score, query)
            interface.print_new_terms(new_terms)
            if new_query == query:
                break
            else:
                query = new_query


if __name__ == "__main__":
    main(sys.argv[1:])
    