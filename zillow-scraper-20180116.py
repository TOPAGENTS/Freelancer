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

#"""################################################################# 3 Get the data by Agent ####################################################################

############ df is the csv file with agent profile url (url doesn't contain the domain) #############
df = pd.read_csv('/Users/payaj/Downloads/zillow-bronx-agents-20180117.csv', dtype='unicode')
driver = webdriver.Chrome(executable_path = path_to_chromedriver)

######### Below first for loop open the profile of each agent(one by one) in the browser ##########

for index in range(1):#for index in range(522,len(df)):
    print df.loc[index,'SellersAgent1Url']
    totalPage = ''
    pages = ''
    page = ''
    try:
        driver.get('https://www.zillow.com'+df.loc[index,'SellersAgent1Url'])
        time.sleep(1)
        driver.get('https://www.zillow.com'+df.loc[index,'SellersAgent1Url'])
        time.sleep(2)

        print "done scrolling"
        soup = BeautifulSoup(driver.page_source, 'html.parser')


        totalPage = soup.findAll('section', {'class': 'sales-history property-listings zsg-content-section'})[0].findAll('ul', {'class': 'pagination zsg-pagination'})[0]
        print 'Stage 1'

        Reference = 0
        for page in totalPage.findAll('a'):
            #pages.append(str(page.text))
            page = int(str(page.text))

        print "Stage 2"
    except:
        print "Nothing on the page"
    if page != '':
        element = driver.find_element_by_xpath("//section[@class='sales-history property-listings zsg-content-section']//a[text()=1]")
    else:
        element = driver.find_element_by_xpath("//section[@class='sales-history property-listings zsg-content-section']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)
    if page > 20:
        page = 20
    if page == '':
        page = 1
    pages = range(1,page+1)
    page = ''
    for page in pages:
        soup = ''
        table = ' '
        try:
            driver.find_element_by_xpath("//section[@class='sales-history property-listings zsg-content-section']//a[text()="+str(page)+"]").click()
            time.sleep(1)
            driver.find_element_by_xpath("//section[@class='sales-history property-listings zsg-content-section']//a[text()=" + str(page) + "]").click()
            driver.find_element_by_xpath("//section[@class='sales-history property-listings zsg-content-section']//a[text()=" + str(page) + "]").click()
            time.sleep(1)
            driver.find_element_by_xpath("//section[@class='sales-history property-listings zsg-content-section']//a[text()=" + str(page) + "]").click()
            driver.find_element_by_xpath("//section[@class='sales-history property-listings zsg-content-section']//a[text()=" + str(page) + "]").click()
            time.sleep(1)
            print "Stage 3"
        except:
            print "No next"

        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.findAll('div', {'class': 'sales-history-table zsg-content-item property-listings-body'})[0].findAll('div', {'class': 'sh-row-body'})[0]
            print "Stage 4"
        except:
            print "Nothing in table"

        for i in range(len(table)):
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
                with open('/Users/payaj/Downloads/zillow-warnerLewis-transactions-20180209.csv', 'a') as outfile:
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
