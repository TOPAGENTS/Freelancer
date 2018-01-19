import time
from bs4 import BeautifulSoup
import csv
import requests
from lxml import html
import sys
import pandas as pd
import random
import re
import csv
from urllib import pathname2url

from selenium.webdriver.support.ui import WebDriverWait
from telnetlib import EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


#Zipcode = '08008'
#City = 'Long Beach Township'
#State = 'NJ'

"""######################################### Using Selenium to login the page #########################################

path_to_chromedriver = '/Users/payaj/Downloads/chromedriver'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
urldefault= 'https://www.redfin.com/TX/Richland-Hills/Undisclosed-address-76118/home/3229900'
browser.get(urldefault)
time.sleep(120)

#browser.find_element_by_link_text('Sign In').click()
#wait = WebDriverWait(browser, 10)


#field1 = wait.until(EC.element_to_be_clickable((By.NAME, "emailInput")))
#browser.execute_script("arguments[0].click();", field1)
#field1.send_keys("in"+ Keys.RETURN)
#field1.send_keys("te"+ Keys.RETURN)
#field1.send_keys("rn"+ Keys.RETURN)
#field1.send_keys("@t"+ Keys.RETURN)
#field1.send_keys("op"+ Keys.RETURN)
#field1.send_keys("ag"+ Keys.RETURN)
#field1.send_keys("en"+ Keys.RETURN)
#field1.send_keys("ts"+ Keys.RETURN)
#field1.send_keys(".n"+ Keys.RETURN)
#field1.send_keys("yc"+ Keys.RETURN)

#field2 = wait.until(EC.element_to_be_clickable((By.NAME, "passwordInput")))
#browser.execute_script("arguments[0].click();", field2)
#field2.send_keys("8"+ Keys.RETURN)
#field2.send_keys("z"+ Keys.RETURN)
#field2.send_keys("WQ"+ Keys.RETURN)
#field2.send_keys("9W"+ Keys.RETURN)
#field2.send_keys("l"+ Keys.RETURN)
#field2.send_keys("L"+ Keys.RETURN)
#field2.send_keys("kG"+ Keys.RETURN)

#### intern@topagents.nyc
#### 8zWQ9WlLkG

#time.sleep(0.5 * random.random())
#browser.find_element_by_class_name('submitButtonWrapper').click()
#soup = BeautifulSoup(browser.page_source, 'html.parser')#"""
proxies = {'http': 'http://topagenets:Topagents1@us-wa.proxymesh.com:31280', 'https': 'http://topagenets:Topagents1@us-wa.proxymesh.com:31280'}
headers = {'User-agent': 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3'}
"""
try:
    for page in range(1,19):
        redfinUrl = requests.get(url='https://www.redfin.com/school/73554/NJ/Ship-Bottom/Long-Beach-Island-Elementary-School/filter/include=sold-3yr,viewport=39.76191:39.74356:-74.10814:-74.13574'+'/page-'+str(page), headers=headers)
        soup = BeautifulSoup(redfinUrl.content, 'html.parser')
        for listing in range(20):
            ListingUrl = ''
            ListingUrl = soup.findAll('div',attrs={'class':'homecard'})[listing].find('a',attrs={'class':'cover-all'}).get('href')


            args = ListingUrl, City, State, Zipcode

            with open('/Users/payaj/Google Drive/redfin-longbeach-20171219/redfin-longbeach-20171219.s15.csv', 'a') as outfile:
                writer = csv.writer(outfile)
                if listing == 0 and page == 1:
                    writer.writerow(["ListingUrl","City", "State", "Zipcode"])
                writer.writerow(args)
        print "page = " + str(page)
        time.sleep(5 * random.random())
except:
    print ("Page = "+str(page) + ", Listing = "+str(listing))#"""

#"""
out = open("/Users/payaj/Google Drive/redfin-scottsdale-s2.csv", 'rb')
df1 = pd.read_csv(out, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
df1 = df1.drop_duplicates('ListingUrl')
df1 = df1.reset_index()
df1 = df1[:10000]

for index in range(7650,len(df1)):
    df1['ListingUrl'] = df1['ListingUrl'].str.replace("http://www.redfin.com","")
    url = 'https://www.redfin.com/'+df1.loc[index,'ListingUrl']
    Unit, Address, ClosingPrice, BuyersCompany = '','','', ''
    DollarSqFt, Neighborhood = '', ''
    State , City, Zipcode = '','',''
    ListingUrl, Beds, SqFt = '','',''
    Baths, SellersCompany1, SellersCompany2 = '','', ''
    Status, ListingPrice, Type = '','',''
    SellersAgent1, SellersAgent2,BuyersAgent = '','',''
    ClosingDate, OriginalPrice, ListedDate = '','',''
    LotSize, YearBuilt, County, Floors = '','','',''

    #"""############################ using scrapper ########################
    resp = requests.get(url=url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(resp.content, 'html.parser')
    webpage = html.fromstring(resp.content)#"""
    """############################ using selenium ########################
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')#"""
    try:
        Beds = str(soup.findAll('div',attrs={'class':'basic-info'})[0].find('span', text=re.compile(r'Beds')).findNext().text)
    except:
        "No Beds"
    try:
        Baths = str(soup.findAll('div',attrs={'class':'basic-info'})[0].find('span', text=re.compile(r'Baths')).findNext().text)
    except:
        "No Baths"
    try:
        Type = str(soup.findAll('div',attrs={'class':'basic-info'})[0].find('span', text=re.compile(r'Style')).findNext().text)
    except:
        "No Type"
    try:
        SqFt = str(soup.findAll('div',attrs={'class':'basic-info'})[0].find('span', text=re.compile(r'Total Sq. Ft.')).findNext().text)
    except:
        "No SqFt"
    try:
        LotSize = str(soup.findAll('div',attrs={'class':'basic-info'})[0].find('span', text=re.compile(r'Lot Size')).findNext().text)
    except:
        "No Lot"
    try:
        YearBuilt = str(soup.findAll('div',attrs={'class':'basic-info'})[0].find('span', text=re.compile(r'Year Built')).findNext().text)
    except:
        "No YearBuilt"
    try:
        County = str(soup.findAll('div',attrs={'class':'basic-info'})[0].find('span', text=re.compile(r'County')).findNext().text)
    except:
        "No County"
    try:
        Floors = str(soup.findAll('div',attrs={'class':'basic-info'})[0].find('span', text=re.compile(r'Floors')).findNext().text)
    except:
        "No Floors"
    try:
        Neighborhood = str(soup.findAll('div',attrs={'class':'keyDetailsContainer'})[0].find('span', text=re.compile(r'Community')).findNext().text)
    except:
        "No Neighborhood"
    try:
        Address = ' '.join(df1.loc[index,'ListingUrl'].split('/')[3].replace('-',' ').split(' ')[:-1]).strip()
    except:
        "No Address"
    try:
        Unit = df1.loc[index,'ListingUrl'].split('/')[4].replace('unit-','').replace('home','').strip()
    except:
        "No Unit"
    try:
        City = df1.loc[index,'ListingUrl'].split('/')[2].replace('-',' ').strip()
    except:
        "No City"
    try:
        State = df1.loc[index,'ListingUrl'].split('/')[1].replace('-',' ').strip()
    except:
        "No State"
    try:
        Zipcode = df1.loc[index,'ListingUrl'].split('/')[3].replace('-',' ').split(' ')[-1].strip()
    except:
        "No Zipcode"
    try:
        ListingUrl = url
    except:
        "No Listingurl"

    try:
        table =''
        table = soup.findAll('table', {"class": 'basic-table-2'})[0]
    except:
        print ("No Table")
    try:
        ClosingDate = str(table.findAll('div', text=re.compile(r'Sold'))[0].findPrevious('td', attrs={'class': 'date-col highlight nowrap'}).text)
    except:
        print ("No ClosingDate")

    try:
        ClosingPrice = str(table.findAll('div', text=re.compile(r'Sold'))[0].findNext('td', attrs={'class': 'price-col number'}).text)
        if '$' in ClosingPrice:
            ClosingPrice = ClosingPrice
        else:
            ClosingPrice = ''
    except:
        print ("No ClosingPrice")

    try:
        ListedDate = str(table.findAll('div', text=re.compile(r'Sold'))[0].findNext('div', text=re.compile(r'Active|Relisted|New|Listed')).findPrevious('td', attrs={'class': 'date-col highlight nowrap'}).text)
    except:
        print ("No ListedDate")
    try:
        OriginalPrice = str(table.findAll('div', text=re.compile(r'Sold'))[0].findNext('div', text=re.compile(r'Active|Relisted|New|Listed')).findNext('td', attrs={'class': 'price-col number'}).text)

        if '$' in OriginalPrice:
            OriginalPrice = OriginalPrice
        else:
            OriginalPrice = ''
    except:
        print ("No OriginalPrice")

    # Get status
    try:
        status1 = soup.findAll("span", {"class": "status-container"})[0]
        Status = str(status1.text)[8:]
    except:
        print ("Unresolved Status")

    # Get Listing Price
    try:
        price = soup.findAll("div", {"class": "info-block price"})[0]
        ListingPrice = price.getText().split("Last", 1)[0]
    except:
        print ("Unresolved ListingPrice")

    # Get Sellers Agent
    try:
        Lister = soup.findAll("div", {"class": "agent-info-item agent-info-item-condensed"})
        SellersAgent2 = Lister[0].getText()
        SellersCompany2 = str(SellersAgent1.split(',')[1].strip())
        SellersAgent2 = str(SellersAgent1.split(',')[0])
    except:
        print ("Unresolved Sellers Agent")

    try:
        Lister = soup.find('h4', text=re.compile(r'Listing provided courtesy of')).findNext().text
        SellersAgent1 = str(Lister.split(',')[0])
        SellersCompany1= str(Lister.split(',')[1].strip())

    except:
        print ("Unresolved Sellers Agent")

    # Get Buyer's Agent

    try:
        Listername = soup.find('h4', text=re.compile(r"Buyer's Agent")).findNext().text
        BuyersAgent = str(Listername.split(',')[0])
        BuyersCompany = str(Listername.split(',')[1].strip())
    except:
        print ("Unresolved Buyers Agent")

    args = Unit, Address, ClosingPrice, DollarSqFt, City, Zipcode, Neighborhood, ListingUrl, Beds, SqFt, State, Baths, Status, ListingPrice, Type, SellersAgent2, SellersAgent1, SellersCompany2, SellersCompany1, BuyersAgent, BuyersCompany, ClosingDate, OriginalPrice, ListedDate, LotSize, YearBuilt, County, Floors

    print "Index = "+str(index)

    with open('/Users/payaj/Google Drive/redfin-scottsdale-scrapeddata-s2.1.csv', 'a') as outfile:
        writer = csv.writer(outfile)
        if index == 0:
            writer.writerow(['Unit', 'Address', 'ClosingPrice', 'DollarSqFt', 'City', 'Zipcode', 'Neighborhood', 'ListingUrl', 'Beds', 'SqFt', 'State', 'Baths', 'Status', 'ListingPrice', 'Type', 'SellersAgent2', 'SellersAgent1', 'SellersCompany2', 'SellersCompany1', 'BuyersAgent', 'BuyersCompany', 'ClosingDate', 'OriginalPrice', 'ListedDate', 'LotSize', 'YearBuilt', 'County', 'Floors'])
        writer.writerow(args)

    if index%100 == 0 :
        time.sleep(10 * random.random())
    else:
        time.sleep(3 * random.random())#"""



#path_to_chromedriver = '/Users/payaj/Downloads/chromedriver'
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--proxy-server=%s' % proxies)


#for i in range(10):
#    print requests.get(url="http://icanhazip.com", proxies=proxies).text
#    print requests.get(url="http://icanhazip.com").text
#    time.sleep(5)