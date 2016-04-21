#!/usr/bin/env python
#See below for code implemented. Code near top originated from PDFMiner
import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

# main
def main(argv):
    import getopt
    def usage():
        print ('usage: %s [-d] [-p pagenos] [-m maxpages] [-P password] [-o output]'
               ' [-C] [-n] [-A] [-V] [-M char_margin] [-L line_margin] [-W word_margin]'
               ' [-F boxes_flow] [-Y layout_mode] [-O output_dir] [-R rotation]'
               ' [-t text|html|xml|tag] [-c codec] [-s scale]'
               ' file ...' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:CnAVM:L:W:F:Y:O:R:t:c:s:')
    except getopt.GetoptError:
        return usage()
    if not args: return usage()
    # debug option
    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    outtype = None
    imagewriter = None
    rotation = 0
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    for (k, v) in opts:
        if k == '-d': debug += 1
        elif k == '-p': pagenos.update( int(x)-1 for x in v.split(',') )
        elif k == '-m': maxpages = int(v)
        elif k == '-P': password = v
        elif k == '-o': outfile = v
        elif k == '-C': caching = False
        elif k == '-n': laparams = None
        elif k == '-A': laparams.all_texts = True
        elif k == '-V': laparams.detect_vertical = True
        elif k == '-M': laparams.char_margin = float(v)
        elif k == '-L': laparams.line_margin = float(v)
        elif k == '-W': laparams.word_margin = float(v)
        elif k == '-F': laparams.boxes_flow = float(v)
        elif k == '-Y': layoutmode = v
        elif k == '-O': imagewriter = ImageWriter(v)
        elif k == '-R': rotation = int(v)
        elif k == '-t': outtype = v
        elif k == '-c': codec = v
        elif k == '-s': scale = float(v)
    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)
    if not outtype:
        outtype = 'text'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout
    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                              imagewriter=imagewriter)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale,
                               layoutmode=layoutmode, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp, codec=codec)
    else:
        return usage()
    for fname in args:
        fp = file(fname, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            page.rotate = (page.rotate+rotation) % 360
            interpreter.process_page(page)
        fp.close()
	currFile = open("output.txt")
	fileString = stripTags(currFile.read())
	formParser(fileString, [["CEEB", "Full Name", "Type", "City", "State", "Country"], ["Spec Curr", "Grade Syst", "Beg", "End", "Dipl/Cert", "Cert Date", "Grad HS?", "Lst Schl"]], 10)
	currFile.close()
    device.close()
    outfp.close()
    return
	
#@Author: Jimmy Cheung
#@Date: April 21st, 2016
#Given a set of tags and a string tag, check whether the tag is in the set.
def isStartTag(set, tag):
	for k in set:
		if tag.startswith(k):
			return True
	return False
#Function with hard-coded tags that opens the file output.txt, reads the data in and maps tags to values
def mapData():
	file = open("output.txt")
	fileString = file.read()
	pageTags = {"School Profile", "Academic Profile", "Student Profile", "Schools Attended", "Exam", "Self-Reported Transcript", "Extracurricular", "Personal Statements"}
	sectionTags = {"School", "School Profile", "School Demographics", "Applicants to UC/UC Berkeley", "College/Major"
	, "Academic Profile", "Student Data", "Other Info", "Birth Info", "Residency", "Languages and Study Abroad", "Guardian 1",
	"Guardian 2", "Guardian Income", "Student Income", "Gap in Education", "SAT", "SAT Subject", "ACT", "AP ()"}
	sectionStartTag = {"Latest High School Averages", "Applicant within Latest High School"}
	equalTags = {"Recommendations","Name", "Organization", "Title", "Relationship", "Phone", "Email", "Waiver", 
	"Waiver Response", "Waiver Signature", "Recommendation Requested", "Recommendation Submitted", "Reference", 
	"Applicant", "Waiver", "Waiver Response", "Waiver Signature", "Requested", "Recommender", "Name", 
	"Organization", "Title", "Relationship", "Phone", "Email", "Submitted"}
	startTags = {"Reference #"}
	finishedDictionary = {}
	currentIndex = 0
	currentText = ""
	currentTag = ""
	currentCat = ""
	dontAppend = False
	while "|||||" in fileString:
		currentIndex = fileString.find("|||||") # Stop at each delimiter
		newText = fileString[:currentIndex].strip()
		print newText
		if newText in equalTags or isStartTag(startTags, newText):
			if currentText == "":
				currentCat = currentTag
			else:
				finishedDictionary[currentCat + " " + currentTag] = currentText.strip()
			currentTag = newText
			currentText = ""
		else:
			currentText = currentText + " " + newText
		fileString = fileString[currentIndex + 5:]
	file.close()
	print finishedDictionary
	return finishedDictionary

#To Run: python setup.py install followed by pdf2txt.py -o output.txt -t tag samples/YourFileHere.pdf
#text is the text to strip other symbols from, primarily < and >
def stripTags(text):
	finalText = ""
	currstartBracket = text.find('<')
	currendBracket = text.find('>')
	while currstartBracket != -1:
		finalText = finalText + text[:currstartBracket]
		text = text[currendBracket + 1:]
		currstartBracket = text.find('<')
		currendBracket = text.find('>')
	print finalText
	return finalText
# parsedText is the text to be parsed, columnList is a list of list of columns needed, numOccurences is how many times the entire section appears		
def formParser(parsedText, columnList, numOccurences):
	currRow = 0
	currOccurence = 1
	currColumn = 0
	finishedList = {}
	while "|||||" in parsedText and currOccurence <= numOccurences:
		currentIndex = parsedText.find("|||||")
		newText = parsedText[:currentIndex].strip()
		#print newText
		if newText not in columnList[currRow] and newText.strip() != "":
			finishedList[columnList[currRow][currColumn] + " " + str(currOccurence)] = newText
			if currColumn == len(columnList[currRow]) - 1:
				currRow = currRow + 1
				currColumn = 0
			if currRow == len(columnList):
				currRow = 0
				currColumn = 0
				currOccurence = currOccurence + 1		
		parsedText = parsedText[currentIndex + 5:]
	print finishedList

if __name__ == '__main__': sys.exit(main(sys.argv))
