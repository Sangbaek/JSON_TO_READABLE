import sys, os, subprocess, argparse, time
import json as json
import xml.etree.ElementTree as ET
import xml.dom.minidom as mindom
from xml.sax.saxutils import unescape
#json and xml modules are already standard at python >2.6
#Sangbaek Lee, Jan. 30 2019
#keep every digit in epochtime in the stamps
#do not use 3rd party libraries if possible e.g. pip
#rss follows xml format with very specific tags: title, link, description(required) + some optional tags (e.g. media, pubDate, guid, url,...)
#
class rss_object:
    def __init__(self, tag_main, title='Test',link='https://clas12mon.jlab.org/status/decoding/',description='description',pubDate=None,guid=None,url=None):
        self.type = "rss_object"
        self.tag_main= tag_main
        self.tag_title= ET.SubElement(self.tag_main,"title")
        self.tag_title.text = title
        self.tag_link = ET.SubElement(self.tag_main,"link")
        self.tag_link.text = link
        self.tag_description = ET.SubElement(self.tag_main,"description")
        self.tag_description.text = unescape(description)
        if pubDate is not None:
            self.tag_pubDate= ET.SubElement(self.tag_main,"pubDate")
            self.tag_pubDate.text = pubDate
        if guid is not None:
            self.tag_guid= ET.SubElement(self.tag_main,"guid")
            self.tag_guid.text = guid
        if url is not None:
            self.tag_url= ET.SubElement(self.tag_main,"url")
            self.tag_url.text = url

#Classes for making the very first rss file.
#Initial Setup of essential components for an RSS feed.
#Call it rss main
class rss_main(rss_object):
    def __init__(self, title="Test: converting a json to an rss file",link='https://clas12mon.jlab.org/status/decoding/',description='main description',save=False,fileout='out.xml'):
        self.type = "rss_main"
        self.tag_namespace  = ET.Element('rss')
        self.tag_namespace.set("version","2.0")
        self.tag_channel = ET.SubElement(self.tag_namespace,"channel")
        #sub objects under channel
        rss_object.__init__(self,self.tag_channel, title,link,description)
        if fileout is None:
            self.fileout = fileout
        if save is True:
            self.savexml(fileout)
#a simple ftn to write rss file
    def savexml(self,fileout=None):
        if fileout is None:
            fileout=self.fileout
        self.dom=mindom.parseString(ET.tostring(self.tag_namespace))
        self.prettyprint=self.dom.toprettyxml()
        self.prettyprint= self.prettyprint.replace("&quot;","\"")
        outfile = open(fileout,"w")
        outfile.write(unescape(self.prettyprint))
        outfile.close()

# add rss object
    def add_item(self, title='item_title',link='https://clas12mon.jlab.org/status/decoding/',description='item_description',pubDate=None,guid=None,url=None,save=False, fileout='out.xml'):
        self.tag_item = ET.SubElement(self.tag_channel,"item")
        self.item = rss_object( self.tag_item,title,link,description, pubDate, guid, url)
        self.dom=mindom.parseString(ET.tostring(self.tag_namespace))
        self.prettyprint=self.dom.toprettyxml()
        if save is True:
            savexml(fileout)

def nodoublelinebreak(string):
    target_string=['\n\n','\n\t\n\t','\n\t\t\n\t\t','\n\t\t\t\n\t\t\t']#,'\n\t\t\t\t\n\t\t\t\t']
#     desired_string = ['\n','\n\t','\n\t\t','\n\t\t\t']#,'\n\t\t\t\t']
    for i in range(0,len(target_string)):
        while string.find(target_string[i]) >= 0:
            string = string[:string.find(target_string[i])]+string[string.find(target_string[i])+i+1:]
    return string

#Modify an rss file existing and add some items
class rss_modify(rss_object):
    def __init__(self, title='item_title',link='https://clas12mon.jlab.org/status/decoding/',description='item_description',pubDate=None,guid=None,url=None,save=False, item_add = False, filein = 'in.xml', fileout=None):
        self.type = "rss_modify"
        self.tree = ET.parse(filein)
        self.tag_namespace = self.tree.getroot()
        self.tag_channel = self.tag_namespace[0]
        self.filein = filein
        self.fileout = fileout
#         self.dom=mindom.parseString(ET.tostring(self.tag_namespace))
        self.prettyprint=ET.tostring(self.tag_namespace)
        if item_add is True:
            self.tag_item = ET.SubElement(self.tag_channel,"item")
            self.item = rss_object( self.tag_item,title,link,description, pubDate, guid, url)
            self.add_item(title,link,description,pubDate,guid,url)
        if fileout is None:
            self.fileout = self.filein
        if save is True:
            self.savexml(self.fileout)

    def savexml(self,fileout=None):
        if fileout is None:
            fileout=self.fileout
        outfile = open(fileout,"w")
        self.prettyprint = nodoublelinebreak(str(self.prettyprint))
        if self.prettyprint.find('\n\t\n</rss>')>0:
            self.prettyprint=self.prettyprint[:self.prettyprint.find('\n\t\n</rss>')]+self.prettyprint[self.prettyprint.find('\n\t\n</rss>')+2:]
        self.prettyprint= self.prettyprint.replace("&quot;","\"")
        self.prettyprint=self.prettyprint.replace('&lt;![CDATA[','')
        self.prettyprint=self.prettyprint.replace(']]&gt;','')
        self.prettyprint=self.prettyprint.replace("&lt;TABLE", "<![CDATA[<TABLE")
        self.prettyprint=self.prettyprint.replace("&lt;/TABLE&gt;", "</TABLE>]]>")
        outfile.write(unescape(self.prettyprint))
        outfile.close()

    def add_item(self, title='item_title',link='https://clas12mon.jlab.org/status/decoding/',description='item_description',pubDate=None,guid=None,url=None,save=False, fileout=None):
        self.tag_item = ET.SubElement(self.tag_channel,"item")
        self.item = rss_object( self.tag_item,title,link,description, pubDate, guid, url)
        self.dom=mindom.parseString(ET.tostring(self.tag_namespace))
        self.prettyprint=self.dom.toprettyxml()
        self.prettyprint = nodoublelinebreak(str(self.prettyprint))
        if self.prettyprint.find('\n\t\n</rss>')>0:
            self.prettyprint=self.prettyprint[:self.prettyprint.find('\n\t\n</rss>')]+self.prettyprint[self.prettyprint.find('\n\t\n</rss>')+2:]
        if fileout is None:
            fileout=self.fileout
        if save is True:
            savexml(fileout)

def json_data(myjsonfile):
  try:
    json_data = json.load(myjsonfile)
  except ValueError, e:
    return False
  return json_data
