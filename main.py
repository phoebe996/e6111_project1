import sys
import search
import parser
import interface

def main(argv):
    query = argv[0]
    search_engine = search.SearchEngine()
    xml = search_engine.search(query)
    result = parser.parse_xml(xml)
    interface.print_parameters(search_engine.getKey(), query, search_engine.getUrl())
    score_array, precision = interface.interact(result)
    interface.print_transcript(precision, search_engine.getQuery())
    


    # for ans in result:
    #     print ans.getTitle()
    #     print ans.getDescription()
    #     print '--------------------'

if __name__ == "__main__":
    main(sys.argv[1:])
    