import json
import sys
import os
import requests
import pandas as pd
import time
import re
import time
from bs4 import BeautifulSoup
import random
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
path_to_chromedriver = '/Users/payaj/Downloads/chromedriver'

proxies = {'http': 'http://topagenets:Topagents1@us-wa.proxymesh.com:31280', 'https': 'http://topagenets:Topagents1@us-wa.proxymesh.com:31280'}
headers = {'User-agent': 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3'}



"""################################################################# 1 Get the region ID ####################################################################
getregionid = requests.get('http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id=X1-ZWz1994anr3rij_6ikyi&state=NY&city=10460', headers=headers).content
soup = BeautifulSoup(getregionid, 'lxml')

regions = soup.findAll('list')
regions = regions[0]

regionid = []
for region in regions.findAll('id'):
    regionid.append(region.text)

regionname = []
for region in regions.findAll('name'):
    regionname.append(region.text)

len(regionname)

df = pd.DataFrame(columns=['RegionID', 'Zipcode'], index=range(len(regionname)))
df['RegionID'] = regionid
df['Zipcode'] = regionname

zips = pd.read_csv('/Users/payaj/Downloads/NYC_City.csv', dtype='unicode')
df = pd.merge(df,zips, how='left',on='Zipcode')

with open('/Users/payaj/Downloads/ZillowRegionId-20180106.csv', 'w') as outfile:
    df.to_csv(outfile, sep=',')#"""

"""################################################################# 2 Get the Agent Url ####################################################################
df = pd.read_csv('/Users/payaj/Downloads/ZillowRegionId-20180106.csv', dtype='unicode')
df = df[df['City']=='Bronx']
df = df.reset_index()

for i in range(1,len(df)):
    Reference = 0
    for Page in range(1,26):
        Agents=requests.get('https://www.zillow.com/new-york-ny-'+df.loc[i,'Zipcode']+'/real-estate-agent-reviews/?page='+str(Page)+'&showAdvancedItems=false&regionID='+df.loc[i,'RegionID']+'&locationText=Bronx%20New%20York%20NY%20'+df.loc[i,'Zipcode'], headers=headers).content

        soup = ''
        soup = BeautifulSoup(Agents, 'html.parser')

        AgentCards, SellersAgent1, SellersAgent1Url, SellersAgent1Phone = "", "", "", ""
        AgentCards = soup.findAll('div', {'class':'ldb-contact-summary ldb-fg'})
        for j in range(len(AgentCards)):
            SellersAgent1Url= str(AgentCards[j].findAll('a')[0].get('href'))
            SellersAgent1 = str(AgentCards[j].findAll('a')[0].text)
            SellersAgent1Phone = str(AgentCards[j].findAll('p', {'class':'ldb-phone-number'})[0].text)

            args = SellersAgent1, SellersAgent1Url, SellersAgent1Phone
            with open('/Users/payaj/Downloads/zillow-'+df.loc[i,'Zipcode']+'-AgentUrl.csv', 'a') as outfile:
                writer = csv.writer(outfile)
                if i == 0 and j == 0:
                    writer.writerow(
                        ['SellersAgent1', 'SellersAgent1Url', 'SellersAgent1Phone'])
                writer.writerow(args)

            if Page != Reference:
                time.sleep(10 * random.random())
            Reference = Page
    print ("region index: "+ str(i))#"""

#"""################################################################# 3 Get the data by Agent ####################################################################
df = pd.read_csv('/Users/payaj/Downloads/zillow-bronx-agents-20180117.csv', dtype='unicode')
driver = webdriver.Chrome(executable_path = path_to_chromedriver)

for index in range(12,len(df)):
    print df.loc[index,'SellersAgent1Url']
    try:
        time.sleep(5)
        driver.get('https://www.zillow.com'+df.loc[index,'SellersAgent1Url'])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        totalPage=''

        totalPage = soup.findAll('section', {'class': 'sales-history property-listings zsg-content-section'})[0].findAll('ul', {'class': 'pagination zsg-pagination'})[0]
        print 'Stage 1'
        pages = ''
        Reference = 0
        for page in totalPage.findAll('a'):
            #pages.append(str(page.text))
            page = int(str(page.text))
        pages = range(1,page+1)
        page = ''
        print "Stage 2"
    except:
        print "Nothing on the page"

    for page in pages:
        time.sleep(2)
        soup = ''
        table = ' '
        try:
            #wait = WebDriverWait(driver, 10)
            #NextButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='sales-history property-listings zsg-content-section']//a[text()="+str(page)+"]")))
            #driver.execute_script("arguments[0].click();", NextButton)
            driver.find_element_by_xpath("//section[@class='sales-history property-listings zsg-content-section']//a[text()="+str(page)+"]").click()
            print "Stage 3"
        except:
            print "No next"

        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(2)
            table = soup.findAll('div', {'class': 'sales-history-table zsg-content-item property-listings-body'})[0].findAll('div', {'class': 'sh-row-body'})[0]
            print "Stage 4"
        except:
            print "Nothing in table"

        for i in range(len(table)):
            time.sleep(3)
            Address, City, State, Zipcode, ListingUrl = "","","","",""
            Represent, SellersAgent1, BuyersAgent, ClosingDate, ClosingPrice = "", "", "", "", ""
            ClosingPrice2, SellersAgent1Url = "", ""
            try:
                Address = table.findAll('span', {'class': 'address-line address-street'})[i].text
            except:
                print ("No Address")
            try:
                City =  str(table.findAll('span', {'class': 'address-line address-city-state-zip'})[i].text).split(',')[0].strip()
                State =  str(table.findAll('span', {'class': 'address-line address-city-state-zip'})[i].text).split(',')[1].strip().split(' ')[0]
                Zipcode = str(table.findAll('span', {'class': 'address-line address-city-state-zip'})[i].text).split(',')[1].strip().split(' ')[1]
            except:
                print ("No City, State and Zip")
            try:
                ListingUrl = str(table.findAll('span', {'class': 'address-line address-city-state-zip'})[i].findPrevious('a').get('href'))
            except:
                print ("No ListingURL")
            try:
                Represent = str(table.findAll('div', {'class': 'zsg-lg-1-5 zsg-md-1-3 zsg-sm-1-3 sh-rep sh-cell'})[i].text)
                if Represent == 'Both':
                    SellersAgent1 = df.loc[index, 'SellersAgent1']
                    BuyersAgent = df.loc[index, 'SellersAgent1']
                if Represent == 'Seller':
                    SellersAgent1 = df.loc[index, 'SellersAgent1']
                    BuyersAgent = ''
                if Represent == 'Buyer':
                    SellersAgent1 = ''
                    BuyersAgent = df.loc[index, 'SellersAgent1']
            except:
                print ("No Agent")
            try:
                SellersAgent1Url = df.loc[index, 'SellersAgent1Url']
            except:
                print "No Sellers"
            try:
                ClosingDate = str(table.findAll('div', {'class': 'zsg-lg-1-5 zsg-md-2-3 zsg-sm-2-3 sh-sold-date sh-cell'})[i].text)
            except:
                print ("No ClosingDate")
            try:
                ClosingPrice = str(table.findAll('div', {'class': 'zsg-lg-1-5 zsg-md-1-3 zsg-sm-1-3 sh-sold-price sh-cell'})[i].text.strip().split(' ')[0])
            except:
                print ("No ClosingPrice")
            try:
                ClosingPrice2 = str(table.findAll('div', {'class': 'zsg-lg-1-5'})[i].text)
            except:
                print ("No ClosingPrice2")

            try:
                args = Address, City, State, Zipcode, ListingUrl, SellersAgent1, BuyersAgent, ClosingDate, ClosingPrice, ClosingPrice2, SellersAgent1Url
                with open('/Users/payaj/Downloads/zillow-agenttransactions-20180117.csv', 'a') as outfile:
                    writer = csv.writer(outfile)
                    if Reference == 0:
                        writer.writerow(["Address", "City", "State", "Zipcode", "ListingUrl", "SellersAgent1", "BuyersAgent", "ClosingDate", "ClosingPrice", "ClosingPrice2", "SellersAgent1Url"])
                    writer.writerow(args)
            except:
                print "Nothing to write"
            if page % 10 == 0:
                time.sleep(10 * random.random())
            Reference = page
        print ("page index: " + str(page))#"""




driver.get('https://www.zillow.com'+df.loc[1,'SellersAgent1Url'])
'https://www.zillow.com'+df.loc[12,'SellersAgent1Url']

wait = WebDriverWait(driver, 10)
NextButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='sales-history property-listings zsg-content-section']//a[text()=2]")))
driver.execute_script("arguments[0].click();", NextButton)

