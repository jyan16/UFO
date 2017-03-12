import urllib3
import re
import csv

url = 'http://www.nuforc.org/webreports/'
http = urllib3.PoolManager()
check_list = ['ndxl.html', 'ndxlAB.html', 'ndxlBC.html', 'ndxlHI.html', 'ndxlMB.html', 'ndxlNB.html',
              'ndxlNF.html', 'ndxlNS.html', 'ndxlNT.html', 'ndxlON.html', 'ndxlPQ.html', 'ndxlSA.html',
              'ndxlYK.html', 'ndxlYT.html', 'ndxlSK.html', ]
#get href by month
r_month = http.request('GET', url + 'ndxloc.html')
pattern_month = re.compile(r'COLOR=#000000><A HREF= .+?.html>')
match_month = pattern_month.findall(str(r_month.data))
clean_month = [item[23:-1] for item in match_month]



file_ufo = open('../../data/file_ufo.csv', 'w', encoding='utf-8')
writer = csv.writer(file_ufo)
writer.writerow(['basic information'])
file_ufo.close()

i=1
for item in clean_month:
    #open csv writer
    file_ufo = open('file_ufo.csv', 'a+', encoding='utf-8')
    writer = csv.writer(file_ufo)
    #pass places that are not in US
    if item in check_list:
        continue;
    #get date
    match_date_list = []
    r_date = http.request('GET', url + item)
    pattern_date = re.compile(r'<TR VALIGN=TOP>.+?</TR>')
    match_date = pattern_date.findall(str(r_date.data))

    #record html address for each event
    for subitem in match_date:
        try:
            writer.writerow([subitem.encode('utf-8')])
        except:
            print('error at '+str(i))
        print(i)
        i += 1

    #close csv file
    file_ufo.close()



