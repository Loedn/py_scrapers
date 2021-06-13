#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 13:24:45 2021

@author: loedn
"""
import pandas as pd
import urllib.request
import bs4 as bs
import time
import re

base_url = 'https://theswitchfix.co/product-category/' # base url that will serve as root

writer = pd.ExcelWriter('theswitchfix.xlsx') # modify the name between the '' always add the '.xlsx' suffix so that it knows to write an excel file, the name can be whatever you want, the file will be written in the same directory of this file

# initialize list of lists 
data = [] 
  
# case for categories and items in categories
categories = ["shampoo-bars", "deep-conditioners", "hair-oils", "skincare", "special-edition", "oral-and-lip-care", "combos-and-bundles-haircare"] # these category names are taken from the url 
for c in categories: # loop categories so you'll start searching from base_url+categories[0]
    data = []
    url = f'{base_url}{c}/'
    print(url)
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen( req )
    #time.sleep(5)
    source = con.read()
    soup = bs.BeautifulSoup(source,'lxml')
    cat = soup.body #here you scrape the entire page
    print(url)
    for a in cat.find_all('a', href=True, class_='elementor-button-link'): # from the entire scraped page you get only the links to the products modify the class_='' decorator with a unique class that only the links to products have
        prod = []
        url_builder = a['href'] # here you create the link for the product
        print(url_builder)
        req = urllib.request.Request(url_builder, headers={'User-Agent' : "Magic Browser"}) 
        con = urllib.request.urlopen( req ) #go to the page
        prod_soup =bs.BeautifulSoup(con.read(), 'lxml')
        prod_page = prod_soup.body # scrape the whole product page
        #time.sleep(2)
        
        #Name --> search for value you want ***modify within the find for html tag and class of the data you want*** 
        try:
            prod_name = prod_page.find('h1', class_='product_title')
            prod.append(prod_name.text.strip())
        except: 
            prod.append('no name')
        #Price --> search for value you want ***modify within the find for html tag and class of the data you want***
        try:
            prod_price = prod_page.find('span', class_='woocommerce-Price-amount amount')
            print(prod_price)
            prod_price = re.sub("[^0-9]", "", prod_price.text)
            prod.append(prod_price)
        except: 
            prod.append('no price')
        #Size --> search for value you want ***modify within the find for html tag and class of the data you want***
        try:
            prod_size = prod_page.find('tr', class_='woocommerce-product-attributes-item--weight')
            prod.append(prod_size.text.strip().replace('Weight', '')) #this if you want to sanitize the data --> a weight is "Weight 65kg" and want to remove the "Weight" part if not needed use prod.append(prod_size) 
        except: 
            prod.append('no size')

        #About --> search for value you want ***modify within the find for html tag and class of the data you want***
        try:
            prod_about = prod_page.find('div', class_='woocommerce-product-details__short-description')
            prod.append(prod_about.strip().text)
        except: 
            prod.append('no about')
        prod.append(url_builder)
        data.append(prod)
        
        
    df = pd.DataFrame(data, columns = ['Name', 'Price', 'Size', 'Description', 'url'])
    df.to_excel(writer,f'{c}')
writer.save()
