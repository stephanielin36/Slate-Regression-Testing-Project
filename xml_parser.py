"""
The XML Parser.
@author: koshy1
Last date edited:  April 21, 2016

Use case:
    1.  Place XML in some place - "PATH"
    2.  python xml_parser.py "PATH"
    3.  If no "PATH" specified, checks in cwd for example.xml
    4.  Optionally, pipe output into a text file to see result:
            python kek.py "PATH" > example.txt
Returns:
    dict {
        "XML_PATH1" : ("Value1", "Value2", ...),
        "XML_PATH2" : ("Value1",),
        ...,
    }
"""

from pprint import pprint
import sys
import xml.dom.minidom as md


def filterXML(child_nodes):
    """
    Converts a list of nodes with extraneous garbage:
        In = [
            <DOM Test Node "\n    ">,
            <DOM Element: ...>,
            miscellaneous garbage,
            ...,
        ]
    To a list of nodes filtered by element:
        Out = [
            <Dom Element: ...>,
            <Dom Element: ...>,
            ...,
        ]
    """
    return filter(
        lambda x: x.nodeType == x.ELEMENT_NODE,
        child_nodes,
    )


def flattenXML(elements, path, flat={}):
    """
    Converts a nested XML:
        In = [
            <Dom Element: A>
                <Dom Element: B>
                    ... valB ...
                </Dom Element: B>
                <Dom Element: C>
                    ... valC ...
                </Dom Element: C>
                ...
            </Dom Element: A>,
        ]
    To a flattened recursive dictionary of element-value pairs:
        Out = {
            "B": valB,
            "C": valC,
        }
    If multiple elements have the same name:
        Out = {
            "EducationSubtestCode": (English, Writing, ...),
            "ScoreValue": (31, 30, ...),
        }
    """
    # Iterate and recurse.
    for el in filterXML(elements):
      
      # Base case 1: empty nest
      size = el.childNodes.length
      
      if size == 0:
          continue
      # Base case 2: nest of text

      node = el.childNodes[0]
      if size == 1 and node.nodeType == node.TEXT_NODE:
          # Create tuple
          new_path = path + el.tagName + "/"
          if new_path not in flat:
              flat[new_path] = [node.nodeValue]
          else:
              flat[new_path] += [node.nodeValue]
          continue
      new_path = path + el.tagName + "/"
      flattenXML(filterXML(el.childNodes), new_path, flat)
    return flat


def parseXML():
    # Saves "PATH" to XML file.
    if len(sys.argv) > 1:
        xml_path = sys.argv[1]
    else:
        #REPLACE "example.xml" with XML that you want parsed
        xml_path = "example.xml"

    # Reads in the XML document.
    test_xml = md.parse(xml_path)

    # Dictionary of Data Fields.
    XML_dictionary = dict()

    # """
    # If this exists, overwrites later student-submitted scores.
    #     <UCPerson>
    #         <OfficialTestScores>
    #             ...
    #         </OfficialTestScores>
    #     </UCPerson>
    # """
    # for ots in test_xml.getElementsByTagName('OfficialTestScores'):
    #     data = filterXML(ots.childNodes)
    #     XML_dictionary.update(flattenXML(data))

    """
    Change this depending on which nodes need to be defined beyond its parent.
        XML_dictionary["Parent of Parent"] = flattenkek(...)
    """
    XML_dictionary.update(flattenXML(test_xml.getElementsByTagName("UCRecords"), ""))
    
    return XML_dictionary

XML_dictionary = parseXML()
pprint(XML_dictionary)

