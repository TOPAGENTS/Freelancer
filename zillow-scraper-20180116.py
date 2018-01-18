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


#"""################################################################# 3 Get the data by Agent ####################################################################

############ df is the csv file with agent profile url (url doesn't contain the domain) #############
df = pd.read_csv('/Users/payaj/Downloads/zillow-bronx-agents-20180117.csv', dtype='unicode')
driver = webdriver.Chrome(executable_path = path_to_chromedriver)

######### Below first for loop open the profile of each agent(one by one) in the browser ##########
for index in range(12,len(df)):
    print df.loc[index,'SellersAgent1Url']
    try:
        time.sleep(5)
        driver.get('https://www.zillow.com'+df.loc[index,'SellersAgent1Url'])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        totalPage=''
        
        ######## below code will find the pagination footer of the "past sales" table (2nd table) ########
        totalPage = soup.findAll('section', {'class': 'sales-history property-listings zsg-content-section'})[0].findAll('ul', {'class': 'pagination zsg-pagination'})[0]
        print 'Stage 1'
        pages = ''
        Reference = 0
        ########### below for loop will get the last number of the page in the "past sales" table and save it in page in integer format##############################
        ######################### then will save all the page number in "pages"
        for page in totalPage.findAll('a'):
            #pages.append(str(page.text))
            page = int(str(page.text))
        pages = range(1,page+1)
        page = ''
        print "Stage 2"
    except:
        print "Nothing on the page"
        
    ######## below for loop will call all the page numbers inside "pages" one by one ########
    for page in pages:
        time.sleep(2)
        soup = ''
        table = ' '
        
        ############## below code will click on the page number of the "past sales" table based on the for loop #############
        try:
            #wait = WebDriverWait(driver, 10)
            #NextButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='sales-history property-listings zsg-content-section']//a[text()="+str(page)+"]")))
            #driver.execute_script("arguments[0].click();", NextButton)
            driver.find_element_by_xpath("//section[@class='sales-history property-listings zsg-content-section']//a[text()="+str(page)+"]").click()
            print "Stage 3"
        except:
            print "No next"
        ############### below section will have the html code for the table #################
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(2)
            table = soup.findAll('div', {'class': 'sales-history-table zsg-content-item property-listings-body'})[0].findAll('div', {'class': 'sh-row-body'})[0]
            print "Stage 4"
        except:
            print "Nothing in table"
        
        ############## below for loop will iterate through the first page of the table and will write the data in the csv (row by row) ##############
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
            ############################### the last for loop for one page of the table (which was writing data in a csv row by row ends here) ##############
        print ("page index: " + str(page))#"""
        ###################### for loop that was changing the pages of the table ends here #######################
   
################### for loop that changes the agent profile from the csv ends here ##########################"""
        
