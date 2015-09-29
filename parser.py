import xml.etree.ElementTree as ET
import re

class SiteInfo:
    def __init__(self):
        self.title = None
        self.description = None
        self.url = None

    def setTitle(self, title):
        self.title = title

    def setDescription(self, des):
        self.description = des

    def setUrl(self, url):
        self.url = url

    def getTitle(self):
        return self.title
    
    def getDescription(self):
        return self.description

    def getUrl(self):
        return self.url

def parse_xml(xml_content):
    tree = ET.parse(xml_content)
    root = tree.getroot()
    result_array = []
    #search <entry> to identify results
    for child in root:
        match = re.search('.*entry$', child.tag)
        if match != None:
            parsed_result = parse_single_site(child)
            result_array.append(parsed_result)
    return result_array

def parse_single_site(entry):
    for content in entry:
        match = re.search('.*content$', content.tag)
        if match != None:
            info = SiteInfo()
            for properties in content[0]:              
                match = re.search('.*Title$', properties.tag)
                if match != None:
                    info.setTitle(properties.text)
                match = re.search('.*Description$', properties.tag)
                if match != None:
                    info.setDescription(properties.text)
                match = re.search('.*Url$', properties.tag)
                if match != None:
                    info.setUrl(properties.text)
            return info
