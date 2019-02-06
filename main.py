from read_json import *

parser = argparse.ArgumentParser()
parser.add_argument('-i','--initialize', action='store_const', dest='mode_val',const='initialize', help='initialize an rss feed')
parser.add_argument('-a','--add', action='store_const', dest='mode_val', const='add', help='add an rss item')
parser.add_argument('-f','--filename', action='store', help='file name e.g. rss.xml')
parser.add_argument('-j','--jsonfilename', action='store', help='file name e.g. rss.xml')

args = parser.parse_args()
if args.mode_val:
    MODE=args.mode_val
else:
    print "Syntax ERROR, please choose a mode."
    exit()

if args.filename and args.jsonfilename:
    filename=args.filename
    jsonfilename=args.jsonfilename
else:
    print "Please put the filename on the command line."
    exit()

#jsonfilename= 'convert_this_to_XML.json'
jsonfilename=args.jsonfilename
jsonfile = open(jsonfilename,'r')

# validate/parse a json file
data = json_data(jsonfile)
jsonfile.close()
if data is False:
    print 'The input file is not a proper json configuration. Check the input file.'
    exit()
# data looks like [dict]. so need to get the dictionary out of the data.
data=data[0]

#initialize rss_description as a form of the table
rss_description = '<![CDATA[<TABLE border style=\"border-collapse: collapse;\">'
rss_description += '<TR><TH>workflow name</TH><TH>jobs</TH>\
<TH>succeeded</TH><TH>success</TH><TH>attempts</TH>\
<TH>phase</TH><TH>dispatched</TH><TH>depend</TH>\
<TH>active</TH><TH>update date</TH><TH>current date</TH></TR><TR>'

#store only the needed information
specific_keys = ['workflow_name','jobs','succeeded','success','attempts','phase','dispatched','auger_depend','auger_active','update_ts','current_ts']
for i in specific_keys:
    dummy= data.get(i)
    if i == 'success':
        if data.get('succeeded'):
            dummy = '%2.1f'%(100.*data.get('succeeded')/data.get('jobs')) +' %'
        else:
            dummy ='0'
    if dummy == None:
        dummy = '0'
    if i[-3:]=='_ts':
        dummy = str(time.strftime("%a, %d %b %Y %H:%M:%S EST", time.localtime(data.get(i)/1000.)))+'\t + %03d ms'%(data.get(i)%1000)
    dummy= str(dummy)
    rss_description += '<TD>' + dummy+'</TD>'
rss_description += '</TR></TABLE>]]>'

if MODE =='initialize':
    main=rss_main(title="CLAS 12 Workflow")
    main.add_item(title=str(data["workflow_name"]),description=rss_description, pubDate=time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(data["update_ts"]/1000))  )
    main.savexml(filename)

if MODE =='add':
    modified=rss_modify(filein=filename)
    # b.tag_channel[3][2].text ='new description'
    modified.add_item(title=str(data["workflow_name"]),description=rss_description, pubDate=time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(data["update_ts"]/1000))  )
    modified.savexml(filename)
