'''
import statements
'''
import pandas as pd
import numpy as np
#used to open URLs
import urllib.request
#used to extract data from html files
import bs4 as bs #use soup = bs.BeautifulSoup(import bs4 as bs #use soup = bs.BeautifulSoup(
from requests import get
import csv# import statements

import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl# import statements
#needed to write from print function
import io

'''
Global functions
'''
#loading dynamic webpage
class Page(QWebEnginePage):    

    app = QApplication(sys.argv) # this variable should be global so it doesn't cause the app to crash when looped
    
    def __init__(self, url):
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

#function to get all info from the product page into contents
def print_to_string(el): 
    output = io.StringIO()
    print(el, file=output)
    contents = output.getvalue()
    output.close()
    return contents
#function to get seperate elements out of content
def getcontentout(string1, string2):
    try:
        thecontent = ((piece2.split(string1)[1]).split(string2))[0]
        return thecontent
    except:
        return None

'''
Scrapes all overview pages in a loop for Hermes bags - 20 pages currently
'''

bags = []
bags.append(['productname','brand','price','pagelink','condition','conditiondetails','exteriorcolor','exteriormaterial','hardware','accessories','brandcode', 'measurements','itemnr','claircode'])

for i in range(1,21): 
    pagenr = str(i)
    urlpage = 'https://shop.rebag.com/collections/Hermes/?page='+pagenr
    print(urlpage)
    req = urllib.request.Request(urlpage)
    # providing a basic user-agent so our scraper doesn't get blocked
    # query the website and return the html to the variable 'page'
    req.add_header('User-Agent', 'Mozilla/5.0')
    page = urllib.request.urlopen(req)
    soup = bs.BeautifulSoup(page, 'html.parser')

    #in the soup find all product cards
    results = soup.find_all('div',attrs={'class': 'product-caption'})
    #check if the results we got corresponds to the number of elements on a page
    print('Number of results', len(results))#in the soup find all product cards 
    counter = 0

    '''
    Scrapes each product on the overview page 
    '''
    for i in range(len(results)):
        counter+=1
        print(counter) 

        #go per item/line of results
        data = results[i]
        
        #extract seperate elements
        page2 = data.find('a',attrs={'class': 'product-price'}).get('href')
        price = data.find('a',attrs={'class': 'product-price'}).getText()
        brand = data.find('a',attrs={'class': 'product-vendor'}).getText()

        #go to product page and scrape productpage into soup2
        url2 ='https://shop.rebag.com'+page2
        nextpage = Page(url2)
        soup2 = bs.BeautifulSoup(nextpage.html, 'html.parser')
        #get info out of soup2, is in javascript within <script> tag
        elements = soup2.find('script',attrs={'data-creator_name': 'Rebag','type': 'application/ld+json'})
        #use function to dump javascript content into a string 
        description_str = print_to_string(elements)
        #use string and list manipulations to extract info seperately
        try:
            list1 = description_str.split("Condition: ")
        except:
            list1 = None
        try:
            piece2 = list1[1]
        except:
             piece2 = None

        #extracts condition and condition details
        try:
            condition = (piece2.split("."))[0]
        except:
            condition = None
        try: 
            conditiondet = ((piece2.split("  Accessories:"))[0]).strip(condition)
        except:
            conditiondet = None
        #use function to extract all other elements seperately
        acc = getcontentout('Accessories: ', '  Measurements:')
        measurem = getcontentout('Measurements: ', ' Designer: ')
        model = getcontentout('Hermes Model: ',' Exterior Material:')  #change for other designers!
        extmat = getcontentout('Exterior Material: ',' Exterior Color:') 
        extcolor = getcontentout('Exterior Color: ',' Interior Material:')
        hardwarecolor = getcontentout('Hardware Color: ',' Brand Code:')
        authcode = getcontentout('Brand Code: ',' Clair Code:')
        itemnr = getcontentout('Item Number: ','",\n        "image":')
        claircode = getcontentout('Clair Code: ','Item Number: ')
        
        #append list with info of each bag
        bags.append([model,brand,price,page2,condition,conditiondet,extcolor,extmat,hardwarecolor,acc,authcode,measurem,itemnr,claircode])
        print(bags[-1])

#print(bags)

# Create csv and write bags list to output file
with open('rebag_hermes.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(bags)

print('data saved to file: completed')


