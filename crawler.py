import urllib3
import re
import csv

url = 'http://www.nuforc.org/webreports/'
http = urllib3.PoolManager()

#get href by month
r_month = http.request('GET', url + 'ndxevent.html')
pattern_month = re.compile(r'COLOR=#000000><A HREF= .+?</A></TD>')
match_month = pattern_month.findall(str(r_month.data))
clean_month = [item[23:-17] for item in match_month]



file_ufo = open('file_ufo.csv', 'w', encoding='utf-8')
writer = csv.writer(file_ufo)
writer.writerow(['basic information'.encode('utf-8'), 'description'.encode('utf-8')])
file_ufo.close()

i=1
for item in clean_month:
    #open csv writer
    file_ufo = open('file_ufo.csv', 'a+', encoding='utf-8')
    writer = csv.writer(file_ufo)

    #get date
    match_date_list = []
    r_date = http.request('GET', url + item)
    pattern_date = re.compile(r'COLOR=#000000><A HREF=.+?</A></TD>')
    match_date = pattern_date.findall(str(r_date.data))
    pattern_date_2 = re.compile(r'<A HREF=.+?>')

    #record html address for each event
    for subitem in match_date:
        tmpmatch = pattern_date_2.findall(subitem)
        match_date_list.append(tmpmatch[0][8:-1])

    #record every event
    for event in match_date_list:
        r_event = http.request('GET', url + event)
        pattern_info = re.compile(r'COLOR=#000000>.+?</FONT></TD>')
        match_info = pattern_info.findall(str(r_event.data))
        writer.writerow([match_info[0].encode('utf-8'), match_info[1].encode('utf-8')])
        print(i)
        i += 1

    #close csv file
    file_ufo.close()



