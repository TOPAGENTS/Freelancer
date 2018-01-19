import pandas as pd
from bs4 import BeautifulSoup
import requests, time
import json
import csv
#Payaj = X1-ZWz1994anr3rij_6ikyi
#bhagyashri = X1-ZWz1961l1bkxe3_5f91a

out = open("/Users/payaj/Google Drive/SouthHampton2017-09-22.csv", 'rb')
df1 = pd.read_csv(out, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

for i in range(len(df1)):
    # Get Zpid and get Zestimate
    Data, Address, ClosingDate, ClosingPrice, ListingUrl = "", "", "", "", ""
    try:
        Data = requests.get("http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-ZWz1961l1bkxe3_5f91a&address="+df1['FormattedAdrress'].str.split(',').str[0][i]+"&citystatezip="+str(df1['City'][i])+"%2C+NY%2C+"+str(df1['Zipcode'][i])).content
    except:
        print "No Zestimate"

    try:
        soup = BeautifulSoup(Data, 'lxml')
    except:
        print "No Soup"

    try:
        Address = df1['Address'][i]
    except:
        print "No Address"

    try:
        ClosingDate = str(soup.find('lastsolddate').text)
    except:
        print "No ClosingDate"

    try:
        ClosingPrice = str(soup.find('lastsoldprice').text)
    except:
        print "No ClosingPrice"

    try:
        ListingUrl = str(soup.find('homedetails').text)
    except:
        print "No URL"

    args = Address, ClosingDate, ClosingPrice

    with open('/Users/payaj/Downloads/southHampton-closingDate-20170925-updated.csv', 'a') as outfile:
        writer = csv.writer(outfile)
        if i == 0:
            writer.writerow(['Address', 'ClosingDate', 'ClosingPrice', 'ListingUrl'])
        writer.writerow(args)

    time.sleep(1)


#Data = requests.get("http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-ZWz1961l1bkxe3_5f91a&address=328+GIN+LANE&citystatezip=Southampton%2C+NY%2C+11968").content

#Data = requests.get("http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-ZWz1961l1bkxe3_5f91a&address=328+Gin+Ln&citystatezip=Southampton%2C+NY%2C+11968").content

