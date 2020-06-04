
import pandas as pd
import numpy as np

import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import bs4 as bs
import urllib.request

import csv

'''
This script scrapes data on Louis Vuitton bags form fashionhpile and writes to a CSV file
IMPORTANT: use pyqt version 5.12 and nor 5.14 (crashes)

Functions for webpage loading and data retrieval:
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

#Get text out of a specific p element in the soup
def getcontent(pcontains):
        try:
            element = (soup2.select_one(pcontains)).getText()
        except:
            element = None
        return element

#Clean a specific element we extracted out of the soup with getcontent()  
def cleancontent(content,tostrip):
    if content != None:
        content = content.strip(tostrip).replace('','')
    return content    

#Extract seperate measurements #mm = measurem
def measuremext(mm):
    (blength, height, width, drop) = (None, None, None, None)
    mlist = mm.split('in')
    mlist.pop()
    
    # Get Base Length - is always first
    blength = mlist[0]
    if 'Length' in blength:
        blength = blength.split(": ")
        blength = blength.pop()
    # Get strap drop - is always last
    if 'Drop' in mlist[-1]:
        drop = mlist[-1]
        drop = (drop.split(": ")).pop()
    # get height and width - are not always in same position of the list
    ind = 0
    while ind < len(mlist):
        if 'Height' in mlist[ind]:
            height = mlist[ind]
            height = (height.split(": ")).pop()
        elif 'Width' in mlist[ind]:
            width = mlist[ind]
            width = (width.split(": ")).pop()
        ind += 1
        
    return (blength, height, width, drop) 

'''
Webscraping multiple webpages in a loop - saving output to a soup object each time -
extracting the relevant info, cleaning up the info, casting info to a list - writing list to csv file

Scraping info on all Louis Vuitton bags from Fashionphile
'''

#Empty list to store content    
bags = []
#append the list with the headers for each column - has to be a string, make sure corresponds to variables at the end
bags.append(['productname','productpage','price','brand','estretailpr','itemnr','category','length','height','width','drop','year',
'acc_included','description','condition','cond_ext','cond_hw','cond_handle','cond_int','cond_other'])

for i in range(1,6): #Loops over different overview pages 'Louis Vuitton bag' - currently 8 pages - blocks in page 6 item 23
    pagenr = str(i)
    urlpage = 'https://www.fashionphile.com/shop/categories/handbag-styles/?brands=louis-vuitton&pageSize=180&sort=date-desc&page='+pagenr
    print(urlpage)
    # open the URL with pyqt5, store info to Soup object with bs
    page = Page(urlpage)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    #find all product cards in the soup
    results = soup.find_all('div',attrs={'class': 'product_container'})
    #creating a counter that tracks scraping of individual product pages
    counter = 0
    print(len(results)) #total number of product pages to scrape

    for result in results: #on each overview page: loops over different product cards to retrieve info of each product
        counter+=1
        print(counter)

        # scrape info of 1 product from overview page
        prname = result.find('h4',attrs={'class': 'product-title'}).getText()
        prpage = result.find('a').get('href')
        price = result.find('span',attrs={'class': 'sale-price'}).getText()
        brand = result.find('h3',attrs={'class': 'brand'}).getText()
        
        #pyqt5 - loads individual product page and saves to soup2
        page2 = Page(prpage)
        soup2 = bs.BeautifulSoup(page2.html, 'html.parser')
        
        # get info out of the soup2 - using my 'getcontent' function defined earlier
        itemnr = getcontent('p:contains("Item #:")')
        measurem = getcontent('p:contains("Measurements")')
        year = getcontent('p:contains("Year:")')
        acc = getcontent('p:contains("Comes With:")')
        descr = getcontent('p:contains("We guarantee this is")')
        cond = getcontent('p:contains("Item Condition:")')
        excond = getcontent('p:contains("Exterior:")')
        condhw = getcontent('p:contains("Hardware:")')
        condhandle = getcontent('p:contains("Handle: ")')
        condint = getcontent('p:contains("Interior: ")')
        condother = getcontent('p:contains("Other: ")')
        try: #get Retail price if present
            estret = (soup2.find('p',attrs={'class': 'est-retail'}).getText()).strip('Est. Retail: $').replace('','')
        except:
            estret = None  
        category = ((soup2.find('ol',attrs={'class': 'breadcrumb'}).getText()).split("\n\n")).pop(-2)  

        #cleaning content with 'cleancontent' function defined earlier
        itemnr = cleancontent(itemnr,'Item #: ')
        (blength, height, width, drop)  = measuremext(measurem) #use predefined function to extract indiv measurements
        year = cleancontent(year,'Year: ')
        cond = cleancontent(cond,'Item Condition: ') # this is still being weird - fix
        excond = cleancontent(excond ,'Exterior: ') 
        condhw = cleancontent(condhw,'Hardware: ')
        condhandle = cleancontent(condhandle,'Handle: ')
        acc = cleancontent(acc,'\nComes With: ')
        condint = cleancontent(condint,'Interior: ')
        condother = cleancontent(condother,'Other: ') 
        category = category[1:]  
        
        # append clean content to the list - make sure order corresponds to headers defined above !!
        bags.append([prname, prpage,price,brand,estret,itemnr,category,blength,height,width,drop,year,
        acc,descr,cond,excond,condhw,condhandle,condint,condother])

#print(bags) #print output of list

# Create csv and write bags list to output file
with open('FP_LVbags.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(bags)

print('data saved to file: completed')