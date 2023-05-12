from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse


import requests
from bs4 import BeautifulSoup
import numpy as np
from itertools import zip_longest
import pandas as pd


listMarques=[]
ListProducts=[]
listTitles=[]
listPrice=[]
listImages=[]
listDiscount=[]
listStars=[]
listLinks=[]
listReviews=[]
listSellerRating=[]
listSellerRatingValue=[]
currentPage=0
numberPages=14

while True:    
    page=requests.get(f"https://www.jumia.com.tn/mlp-telephone-tablette/smartphones/?page={currentPage}#catalog-listing")
    src=page.content
    soup=BeautifulSoup(src,"lxml")

    #numberPages=int((soup.find('p',{'class':'-phs'}).text).split()[0])/40
   
    
    sellerRating=soup.find_all('a',{'class':'fk-rad -me-start','data-eventaction':"seller_score"})


    marques = soup.find_all('a', {'data-eventaction': 'brand'})
    products=soup.find_all('article',{'class':'c-prd'})


    for product in products:
        productTitle=product.find('h3',{'class':'name'})
        listTitles.append(productTitle.text)
        productPrice=product.find('div',{'class':'prc'})
        listPrice.append(productPrice.text)
        if product.find('div',{'class':'stars _s'}) != None:
           listReviews.append(int((product.find('div',{'class':'rev'}).text.strip())[-2]))
        else:
            listReviews.append(0)
        listLinks.append(f"https://www.jumia.com.tn{product.find('a').attrs['href']}")
        listImages.append(product.find('img',{'class':'img'}).attrs['data-src'])
        productDiscount=product.find('div',{'class':'_dsct'})
        if (productDiscount!=None):
            listDiscount.append(int(float(productDiscount.text.rstrip('%'))) )
        else:
            listDiscount.append(0) 

        productStart=product.find('div',{'class':'stars'})
        if productStart != None:
            listStars.append(round(float((productStart.text).split()[0])))    
            #listStars.append(round(float(productStart.text).split))
        else:
            listStars.append(0)
    currentPage+=1
    if currentPage==numberPages:
        break


for rating in sellerRating:
    listSellerRating.append( rating.text)   
    listSellerRatingValue.append( int(rating.text.split('%')[0]))

for marque in marques:
    listMarques.append(marque.text)

dfsellerRating=pd.DataFrame()
dfsellerRating['title']=listSellerRating
dfsellerRating['value']=listSellerRatingValue

#int(rating.text.split('%')[0])
sellerRatingDict=dfsellerRating.to_dict('records')

dfmarques=pd.DataFrame()
dfmarques['marque']=listMarques
marqueDict=dfmarques.to_dict('records')



dfproduct= pd.DataFrame()

dfproduct['name']=listTitles
dfproduct['Discount']=listDiscount                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
dfproduct['stars'] = listStars
dfproduct['price'] = listPrice
dfproduct['image']=listImages
dfproduct['links']=listLinks
dfproduct['review']=listReviews


datalist=dfproduct.to_dict('records')

def index(request):
    paginator = Paginator(datalist, 28)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
       
        marques = request.POST.getlist('marque')
      
        min_value = request.POST.get('min')
      
        
    
    paginator = Paginator(datalist, 28)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/index.html', {'datalist': datalist, 'marqueList': marqueDict, 'sellerRating': sellerRatingDict})

def process_form(request):
    paginator = Paginator(datalist, 28)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':  
        checkbox_value = request.POST.getlist('marque')
        # if 'Vivo' in checkbox_value:
        #     print('Vivo')
        # else:
        #     print(checkbox_value)

        min_value = request.POST.get('min')
        
            
        marques = request.POST.getlist('marque[]')
       

        ratings = request.POST.getlist('rating')
        
        checkbox_values = request.POST.getlist('my_checkbox_name')
       
        ratings=request.POST.getlist('rating')
        
        min=request.POST.get('min')
        max=request.POST.get('max')
      
        return render(request, 'main/index.html', {'datalist': page_obj, 'marqueList': marqueDict, 'sellerRating': sellerRatingDict})
    else:
        return render(request, 'main/index.html', {'datalist': page_obj, 'marqueList': marqueDict, 'sellerRating': sellerRatingDict})

def my_view(request):
    paginator = Paginator(datalist, 28)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        checkbox_values = request.POST.getlist('my_checkbox_name')
       # my_string = "--".join([word.lower() for word in checkbox_values])
      
        
        ratings=request.POST.get('rating')
   
        minprice=request.POST.get('min')
        maxprice=request.POST.get('max')
        
        ratingcheck=request.POST.get('rating')
        page_obj=datalist
        print(listSellerRating)
        #filtered_list = [d for d in page_obj if any(val in d['name'] for val in checkbox_values)]
        if checkbox_values: 
            page_obj = [d for d in datalist if any(val in d['name'] for val in checkbox_values)]
        if minprice:
            page_obj = [d for d in page_obj if ((str(d['price'])).replace(",", "").split()[0])  > (minprice)]
        if maxprice:
            page_obj = [d for d in page_obj if ((str(d['price'])).replace(",", "").split()[0]) < (maxprice)]
        if ratingcheck:
            page_obj= [d for d in page_obj if (int(d['Discount']))  > (int(ratingcheck))    ]
        
        
        #datalist= {name: details for name, details in page_obj. if minprice <= details["price"] <= maxprice}    
    return render(request, 'main/index.html', {'datalist': page_obj, 'marqueList': marqueDict, 'sellerRating': sellerRatingDict})


def chekform(request):
    if request.method == 'POST':
        marques = request.POST.getlist('marque[]')
     
        min_value = request.POST.get('min')
       
    return render(request, 'main/check.html')
def checkboxes(request):
    if request.method=='POST':
        fr=request.POST.getlist('marque[]')
     
    return render(request, 'main/check.html')