from urllib2 import urlopen, URLError
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import datetime as dt

def parse_rows(rows):
    """ Get data from rows """
    results = []
    for row in rows:
        table_headers = row.find_all('th')
        if table_headers:
            results.append([headers.get_text() for headers in table_headers])
        table_data = row.find_all('td')
        if table_data:
            results.append([data.get_text() for data in table_data])
    return results

# month: str; year: int
def extract(month, year):
    if month == 'october' and year == 2012:
        #url = 'http://travel.state.gov/content/visas/english/law-and-policy/bulletin/2013/visa-bulletin-october-2012.html'
        return ['C', '15JUL07']
    if month == 'august' and year == 2006:
        #url = 'http://travel.state.gov/content/visas/english/law-and-policy/bulletin/2006/visa-bulletin-for-August-2006.html'
        return ['C', '01MAR05']
    if month == 'march' and year == 2009:
        #url = 'http://travel.state.gov/content/visas/english/law-and-policy/bulletin/2009/visa-bulletin-march-2009.html'
        return ['C', '15FEB05']
    if month == 'july' and year == 2009:
        return ['C', '01JAN00']
    if month == 'september' and year == 2009:
        return ['C', '08JAN05']
    if month == 'october' and year == 2009:
        return ['C', '22MAR05']
    if month == 'november' and year == 2009:
        return ['C', '01APR05']

    if month ==  "october" or month == "november" or month == "december":
        nextYear = str(year+1)
        url = "http://travel.state.gov/content/visas/english/law-and-policy/bulletin/"+nextYear+"/visa-bulletin-for-"+month+"-"+str(year)+".html"
    else:
        url = "http://travel.state.gov/content/visas/english/law-and-policy/bulletin/"+str(year)+"/visa-bulletin-for-"+month+"-"+str(year)+".html"
    
    try:
        resp = urlopen(url)
    except URLError as e:
        raise Exception("Cannot open url.")

    soup = BeautifulSoup(resp.read(), 'html.parser')        
    try:
        tables = soup.find_all('table')   
    except AttributeError as e:
        raise ValueError("No valid table found.")
    
    eb = 1
    for table in tables:
        #print month, year
        #print table.find('tr').find('td')
        if re.search(r'Employment|Emplyment|Employ-ment', str(table)):
            eb = table
            break
    if eb == 1:
        print "Employment not found", month, year
        exit()
        
    rows = eb.find_all('tr')
    table_data = parse_rows(rows)

    #print url
    #for i in table_data:
    #    print '\t'.join(i)

    cnIndx = -1
    for i in range(len(table_data[0])):
        if re.search(r'CHINA|CH', table_data[0][i]):
            cnIndx = i
            break
    if cnIndx == -1:
        print "China not found", month, year
        exit()

    for i in range(1, len(table_data)):
        if re.search(r'1', table_data[i][0]):
            eb1 = table_data[i][cnIndx]
        elif re.search(r'2', table_data[i][0]):
            eb2 = table_data[i][cnIndx]
            break

    return [eb1, eb2]

#------------------------------------------------------------

months = ["","january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
abrMonth = {'JAN':'1', 'FEB':'2', 'MAR': '3', 'APR': '4', 'MAY': '5', 'JUN':'6', 'JUL':'7', 'AUG':'8', 'SEP':'9', 'OCT':'10', 'NOV':'11', 'DEC':'12'}

f = open("Visa Bulletin Data2.csv", 'w')

for year in range(2010, 2011):
    for i in range(1,13):
        current = "%d,%d,1" % (year, i)
        ebtemp = extract(months[i], year)
        print year, i, ebtemp
        for j in [0,1]:
            if re.match(r'C.*',ebtemp[j]):
                ebtemp[j] = current
            elif re.match(r'U.*',ebtemp[j]):
                continue
            else:
                matchObj = re.match(r'(\d{2})([A-Z]{3})(\d{2}).*', ebtemp[j])
                ebYear = "20" + matchObj.group(3)
                ebMonth = abrMonth[matchObj.group(2)]
                ebDay = matchObj.group(1)
                ebtemp[j] = ebYear+','+ebMonth+','+ebDay                
        f.write("%s\t%s\t%s\n" % (current, ebtemp[0], ebtemp[1]))
    print "Data in %d is collected..." % year

f.close()
print "Done!"
