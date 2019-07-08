import xml.etree.ElementTree as ET

class Extractor(object):
    """description of class"""
    
    def __init__(self, xmlData):

        self.element = ET.fromstring(xmlData)
        #root = tree.getroot()
