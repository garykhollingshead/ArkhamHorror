import json
import xml.dom.minidom as xmlLib

def getXmlFromDictR(json):
	temp = ""
	if type(json) is dict:
		for key in json.keys():
			temp = temp + '<' + key + '>' + str(getXmlFromDictR(json[key])) + '</' + key + '>'
		return temp
	if type(json) is list:
		for x in json:
			temp = getXmlFromDictR(x)
		return temp
	if type(json) is unicode or str:
		return json
	if type(json) is int:
		print "gothere"
		return str(json)

def getXmlFromDict(jsonFilePath, desiredXmlFilePath, rootName):
	r = open(jsonFilePath, 'r')
	s = r.read()
	s = s.replace("\'", "\"")
	print s
	j = json.loads(s)
	r.close()
	x = getXmlFromDictR(j)
	x = '<'+ rootName + '>' + x + '</' + rootName + '>'
	w = open(desiredXmlFilePath, 'w')
	doc = xmlLib.parseString(x)
	doc.writexml(w, '   ', '   ', '\n')
	w.close()
