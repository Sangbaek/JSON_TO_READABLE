CLAS12 WORKFLOW RSS FEED GENERATOR

usage
python main.py -h: help
python main.py -i -f [filename] -j [jsonfilename]
  This will initialize an rss file named "filename" with only one item.
  Suggested filename is "~.xml"           
  If you want to add some item please use the next line.
python main.py -a -f [filename] -j [jsonfilename]
  This will add an item with information stored in "jsonfilename" to the existing rss feed with "filename".
