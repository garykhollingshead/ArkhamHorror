import os

def combineXml(dirPath, resultFilePath, rootName):
    fileNames = os.listdir(dirPath)
    xml = ''
    print "Found:\n" 
    for aFile in fileNames:
        if aFile.find('.xml') > -1:
            print aFile
            r = open(dirPath + '/' + aFile, 'r')
            xml = xml + removeFirstLine(r.read())
            r.close()
    r = open(resultFilePath, 'w')
    r.write("<?xml version=\"1.0\" ?>\n" + '<' + rootName + '>\n' + xml + '</' + rootName + '>')
    r.close()
        

def removeFirstLine(xml):
    return  xml.replace("<?xml version=\"1.0\" ?>", " ")
