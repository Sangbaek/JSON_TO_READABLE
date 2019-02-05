CLAS12 WORKFLOW RSS FEED GENERATOR

usage
python main.py -h: help
python main.py -i -f [filename] -j [jsonfilename]
  This will initialize an rss file named "filename" with only one item.
  Suggested filename is "~.xml"           
  If you want to add some item please use the next line.
python main.py -a -f [filename] -j [jsonfilename]
  This will add an item with information stored in "jsonfilename" to the existing rss feed with "filename".

e.g.)
python main.py -i -f "testfile.xml" -j "rga-decode1_R3432x25_x1300.json"
python main.py -a -f "testfile.xml" -j "rga-decode2_R3464x28_x1300.json"
python main.py -a -f "testfile.xml" -j "rga-decode3_R3750x29_x1300.json"
python main.py -a -f "testfile.xml" -j "rga-decode4_R3501x30_x1300.json"
python main.py -a -f "testfile.xml" -j "rga-decode5_R3355x30_x1300.json"
python main.py -a -f "testfile.xml" -j "rga-decode6_R3466x34_x1300.json"
python main.py -a -f "testfile.xml" -j "rga-decode7_R3249x43_x1300.json"
python main.py -a -f "testfile.xml" -j "rga-decode8_R3191x65_x1300.json"
python main.py -a -f "testfile.xml" -j "rga-decode9_R3135x178_x1300.json" 
