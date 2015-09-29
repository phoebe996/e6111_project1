import sys
import search
import parser

def main(argv):
    key = argv[0]
    xml = search.search_engine(key)
    result = parser.parse_xml(xml)
    for ans in result:
        print ans.getTitle()
        print ans.getDescription()
        print '--------------------'

if __name__ == "__main__":
    main(sys.argv[1:])
    