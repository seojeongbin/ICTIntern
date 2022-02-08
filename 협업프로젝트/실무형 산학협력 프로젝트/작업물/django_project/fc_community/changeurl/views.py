from django.shortcuts import render, redirect
from .models import Url_content
#from .resources import UrlResource
from django.http import HttpResponse
from fcuser.models import Fcuser
from django.views.generic.edit import CreateView
from .forms import Url_content_Form

#using for keyword

import json
from bs4 import BeautifulSoup
from collections import Counter

#________


import time
import random
import requests
import hashlib
import hmac
import base64
import pandas as pd



#using the crawling
import json
import urllib.request
import os
import sys




# Create your views here.


def change(request):
    if request.method =="GET":
        return render(request , 'changeurl.html')
    elif request.method =="POST":
            #세션의 유서에서 유저아이디를 가져와서
            #모델 객체의 user_id와 같은 값을 유저로 가져오는구나.....
        user = Fcuser.objects.get(email=request.session.get('user'))
            #원래 -->user = request.session.get('fcuser') #fcuser 여기 넣고 
        input_image = request.FILES.get('input_image' , None)
        get_url = request.POST.get('get_url' , None)
            #user_name = request.Post.session('')
        url_content = Url_content(
            #모델 안에 있는 변수와 동일시 해주고
        user = user,
        get_url =get_url,
        input_image =input_image,)
        url_content.save()
        #return render(request , 'changeurl.html' , {'input_image' : input_image})
        return redirect('/result/', {'input_image' : input_image}) # result -> changeurl/show



def keyword(request):
    idx = 0
    display = 100
    start =1
    end = 100
    final_result =" "
    final_result_ca = " "
    title_list =[]

    category_list =[]
    category_string = "category"
    
    if request.method == "GET":
        client_id = "xrPeMbf10xfqjK2P4F5h"
        client_secret = "ryuTHmg_Hp"

        #encText = urllib.parse.quote("영양제")
        q = request.GET.get('q')
        
        
        encText = urllib.parse.quote("{}".format(q))
        print(encText)
        url = "https://openapi.naver.com/v1/search/shop?query=" + encText + "&display=" +str(display) + "&start=" + str(start) # json 결과
        naver_api_request = urllib.request.Request(url)
        naver_api_request.add_header("X-Naver-Client-Id",client_id)
        naver_api_request.add_header("X-Naver-Client-Secret",client_secret)

        response = urllib.request.urlopen(naver_api_request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')
            contents = result.get('total') #개수       
                      
            for i in items:                   
                #i가 아이템 한줄
                clean_title_text = BeautifulSoup(i['title'], "lxml").text  #태그가 들어있는 string 에서 <> 사이 내용 제거해주는 코드! 
                title_list.append(clean_title_text)
                #category
                for k in range(1,4,1):
                    category_string+= str(k)
                    cleantext = BeautifulSoup(i[category_string], "lxml").text #태그가 들어있는 string 에서 <> 사이 내용 제거해주는 코드!
                    category_list.append(cleantext)
                    category_string = "category"
                #print(cleantext)
            #________________________
            #결과 분석
            result=[]

            for i in range(len(title_list)):
                result_i = title_list[i].split()
                result += result_i
            
            count = Counter(result)
            tag_count = []
            tags = []
            for n, c in count.most_common(100):
                dics = {'tag': n, 'count': c}
                if len(dics['tag']) >= 2 and len(tags) <= 49:
                    tag_count.append(dics) # 항목별 개수가 저장된 것을 전체 리스트 tag_count에 딕셔너리 하나씩 넣음
                    tags.append(dics['tag'])
            #결과값
            for i in range(0,5,1):
                final_result += tag_count[i]['tag']
                if (i!=4):
                    final_result+= ", "


            #category 
            for i in range(len(category_list)):
                result_i = category_list[i].split()
                result += result_i
            tag_count_ca = []
            tags_ca = []

            for n, c in count.most_common(100):
                dics = {'tag': n, 'count': c}
                if len(dics['tag']) >= 2 and len(tags) <= 49:
                    tag_count_ca.append(dics) # 항목별 개수가 저장된 것을 전체 리스트 tag_count에 딕셔너리 하나씩 넣음
                    tags_ca.append(dics['tag'])

            
            print(tag_count_ca)
            #결과값
            # for i in range(1):
            #     final_result_ca += tag_count_ca[i]['tag']]



             

            #print(title_list)
            
            return render(request , "marketing.html" , {'recommend_keyword': final_result , 'recommend_category' : final_result_ca})   #결과
                
                 
        else:
            print("Error Code:" + rescode) 



#_____________________________________________

def search(request):
    
    idx = 0
    display = 100
    start =1
    end = 100

    if request.method == "GET":
        client_id = "xrPeMbf10xfqjK2P4F5h"
        client_secret = "ryuTHmg_Hp"

        #encText = urllib.parse.quote("영양제")
        q = request.GET.get('q')
        encText = urllib.parse.quote("{}".format(q))
        print(encText)
        url = "https://openapi.naver.com/v1/search/shop?query=" + encText + "&display=" +str(display) + "&start=" + str(start) # json 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
        naver_api_request = urllib.request.Request(url)
        naver_api_request.add_header("X-Naver-Client-Id",client_id)
        naver_api_request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(naver_api_request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            #json.loads(response_body.decode('utf-8))
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')
            contents = result.get('total')
            
            print(contents)
            context = {
                'items': items,
                'input': contents,
                       
                } 
            print("success")
                
            return render(request , "crawling.html" , context = context)       
        else:
            print("Error Code:" + rescode) 





class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())

BASE_URL = 'https://api.naver.com'
API_KEY = '01000000001b4a7367c74e3115b289545caf24cb00a58a4c51df8ab0c9d2cf374cb4b1b00b'
SECRET_KEY = 'AQAAAAAbSnNnx04xFbKJVFyvJMsAV021w58UlPWH3a97fmbUSA=='
CUSTOMER_ID = '2251983' 
uri = '/keywordstool'
method = 'GET'

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
   
    signature = Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


def data_lab(request):
    

    data_analysis = request.GET.get('data_analysis')
    r = requests.get(BASE_URL + uri+'?hintKeywords={}&showDetail=1'.format(data_analysis),
                    headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    df=pd.DataFrame(r.json()['keywordList'])

    df.rename({'compIdx':'경쟁정도',
            'monthlyAveMobileClkCnt':'월평균클릭수_모바일',
            'monthlyAveMobileCtr':'월평균클릭률_모바일',
            'monthlyAvePcClkCnt':'월평균클릭수_PC',
            'monthlyAvePcCtr':'월평균클릭률_PC', 
            'monthlyMobileQcCnt':'월간검색수_모바일',
            'monthlyPcQcCnt': '월간검색수_PC',
            'plAvgDepth':'월평균노출광고수', 
            'relKeyword':'연관키워드'},axis=1,inplace=True)
    df_mini = df.head()
    semi = df_mini.to_html()
    final =semi.replace(" " , "")
    final_2 = final.replace('border="1"','')
    final_3 = final_2.replace("tableclass" , "table class")

    return render(request , "datalab.html" , {'df': final_3})   





            
    
    
    