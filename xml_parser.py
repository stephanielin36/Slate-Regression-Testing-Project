"""
The Kek XML Parser.
Use case:
    1.  Place XML in some place - "PATH"
    2.  python kek.py "PATH"
    3.  If no "PATH" specified, checks in cwd for kek.xml
    4.  Optionally, pipe output into a text file to see result:
            python kek.py "PATH" > kek.txt
Returns:
    dict {
        "Field1" : ("Value1", "Value2", ...),
        "Field2" : ("Value1",),
        ...,
    }
"""

from pprint import pprint
import sys
import xml.dom.minidom as md


def filterkek(child_nodes):
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


def flattenkek(elements, path, flat={}):
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
    for el in filterkek(elements):
      
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
      flattenkek(filterkek(el.childNodes), new_path, flat)
    return flat


def parsekek():
    # Saves "PATH" to XML file.
    if len(sys.argv) > 1:
        xml_path = sys.argv[1]
    else:
        xml_path = "kek.xml"

    # Reads in the XML document.
    kek_xml = md.parse(xml_path)

    # Dictionary of Data Fields.
    kektionary = dict()

    # """
    # If this exists, overwrites later student-submitted scores.
    #     <UCPerson>
    #         <OfficialTestScores>
    #             ...
    #         </OfficialTestScores>
    #     </UCPerson>
    # """
    # for ots in kek_xml.getElementsByTagName('OfficialTestScores'):
    #     data = filterkek(ots.childNodes)
    #     kektionary.update(flattenkek(data))

    """
    Change this depending on which nodes need to be defined beyond its parent.
        kektionary["Parent of Parent"] = flattenkek(...)
    """
    kektionary.update(flattenkek(kek_xml.getElementsByTagName("UCRecords"), ""))
    
    return kektionary

kektionary = parsekek()
pprint(kektionary)

# TODO: Insert specific mappings between data. In what form does PDF parser 
#       expect the data? 
