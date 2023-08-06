import xml.etree.ElementTree as ET


class JazzArtifact():
    def __init__(self, xml: ET.Element):
        self.xml = xml
        if (self.xml is not None):
            self.original_xml_string = ET.tostring(self.xml).decode("utf-8")
        else:
            self.original_xml_string = ""

    def get_text_from_element_path(self, path, namespaces) -> object:
        element = self.xml.find(path, namespaces)
        if (element is not None):
            return element.text

    def get_attribute_from_element_path(self, path, attribute, namespaces) -> object:
        element = self.xml.find(path, namespaces)
        if (element is not None and attribute in element.attrib):
            return element.attrib[attribute]

    def get_attributes_from_element_path(self, path, attributes, namespaces) -> object:
        values = {}
        element = self.xml.find(path, namespaces)
        if (element is not None):
            for attribute in attributes:
                if (attribute in element.attrib):
                    values[attribute] = element.attrib[attribute]
            return values

    def to_string(self) -> str:
        return ET.tostring(self.xml).decode("utf-8")
