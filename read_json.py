import sys, os, subprocess, argparse, time
import json as json
import xml.etree.ElementTree as ET
import xml.dom.minidom as mindom

#json and xml modules are already standard at python >2.6
#Sangbaek Lee, Jan. 30 2019
#keep every digit in epochtime in the stamps
#do not use 3rd party libraries if possible e.g. pip

#jsonfilename= 'convert_this_to_XML.json'
jsonfilename='original.json'
jsonfile = open(jsonfilename,'r')

#Simple function to validate/read data file
def json_data(myjsonfile):
  try:
    json_data = json.load(myjsonfile)
  except ValueError, e:
    return False
  return json_data


data = json_data(jsonfile)
jsonfile.close()
if data is False:
    print 'The input file is not a proper json configuration. Check the input file.'
    exit()

# the json file contains square bracket at the beginning and the end, which is unnecessary for this procedure.
# turn a flag for inserting xml key such as "root" if wanted. (TODO)

def list_to_data(data):
    dummy=data
    while type(dummy) is list and len(dummy)==1:
        if len(dummy)==1:
            dummy = dummy[0]
    return dummy

data = list_to_data(data)
# i=0
# data = dummy
# print 'There are %d unneccessary square bracket(s).'%i
# print 'The default is to ignore these brackets. Turn the flag on for BLAHBLAH(TODO)'

# check the data is restored from json file as dictionary
# print type(data) is dict

#Initial Setup of essential components for an RSS feed.
RSS  = ET.Element('rss')
RSS.set("version","2.0")
RSS_channel = ET.SubElement(RSS,"channel")
RSS_title = ET.SubElement(RSS_channel, "title")
RSS_title.text="Test: converting a json to an rss file"
RSS_link = ET.SubElement(RSS_channel, "link")
RSS_link.text="Not sure about a link"
RSS_description = ET.SubElement(RSS, "description")



# sort the keys and items in alphabetical order
for keys, values in sorted(data.items()):
    if type(values) is list:
        item = ET.SubElement(RSS_channel,"item")
        item_title = ET.SubElement(item, "title")
        item_title.text= keys
        item_link = ET.SubElement(item, "link")
        item_link.text = "Not sure about a link"
        item_description = ET.SubElement(item, "description")
        for i in range(0,len(values)):
            if type(list_to_data(values[i].values())) is list:
                for texts in list_to_data(values[i].values()):
                    if texts is not unicode :
                        texts = str(texts)
                    SubElement2 = ET.SubElement(item,list_to_data(values[i].keys()) )
                    SubElement2.text= texts
            elif type(list_to_data(values[i].values())) is not unicode:
                SubElement2 = ET.SubElement(item,list_to_data(values[i].keys()) )
                SubElement2.text=str(list_to_data(values[i].values()))
            else:
                SubElement2 = ET.SubElement(item,list_to_data(values[i].keys()) )
                SubElement2.text=list_to_data(values[i].values())
    else:
#        SubElement= ET.SubElement(RSS_channel,keys)
        item= ET.SubElement(RSS_channel,"item")
        item_title = ET.SubElement(item,"title")
        item_title.text = keys
        item_link = ET.SubElement(item, "link")
        item_link.text = "Not sure about a link"
        if type(values) is not unicode:
            values=str(values)
        item_description = ET.SubElement(item,"description")
        if keys[-3:]=="_ts":
            values=time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(1548882307000/1000.))+'%03d'%(1548882307001%1000)
        item_description.text=values



dom=mindom.parseString(ET.tostring(RSS))
prettyprint=dom.toprettyxml()
print prettyprint
