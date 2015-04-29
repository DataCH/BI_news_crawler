#-*- coding：utf-8 -*-
#2014-3-12

import urllib2
from bs4 import BeautifulSoup
import time
import re

def get_html(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'};
    request= urllib2.Request(url,headers=headers);

    max_try_num=5
    new_respHtml=None
    for one_try in range(max_try_num):
        try:
            new_resp = urllib2.urlopen(request)
            new_respHtml=new_resp.read()
            break
        except:
            if one_try<=(max_try_num):
                continue
            else:
                print 'Cannot open the url!'
                break
    return new_respHtml

def date_change(date_str):
    date_str=date_str.replace(' ','')
    all_month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    date_list=re.findall(r'(\w{3}).\s{0,5}(\d{1,2}),\s{0,5}(\d{1,2}):(\d{2})\s{0,5}(\w{2})',date_str)
    print date_list
    year='2015'
    month=all_month.index(date_list[0][0])+1
    day=date_list[0][1]
    hour=date_list[0][2]
    minute=date_list[0][3]
    str_day=str(day)
    str_month=str(month)
    str_hour=str(hour)
    str_minute=str(minute)
    if date_list[0][4]=="AM":
        if hour==12:
            hour=0
        if str(hour)==1:
            str_hour='0'+str(hour)
        if str(minute)==1:
            str_minute='0'+str(minute)
        datetime=str(year)+'-'+str(str_month)+'-'+str(str_day)+' '+str(str_hour)+':'+str(str_minute)+':00'
    if date_list[0][4]=="PM":
        if int(hour)==12:
            str_hour=str(hour)
        else:
            hour=int(hour)+12
        str_hour=str(hour)
        if str(hour)==1:
            str_hour='0'+str(hour)
        if str(minute)==1:
            str_minute='0'+str(minute)
        datetime=str(year)+'-'+str(str_month)+'-'+str(day)+' '+str_hour+':'+str(str_minute)+':00'
    return datetime

def main():
    start_page_num=2
    end_page_num=20

    for page_num in range(start_page_num,end_page_num+1):
        url="http://www.businessinsider.com/sai?page="+str(page_num)
        resp_html=get_html(url)

        if type(resp_html)!=type(None):
            print(url)

            #catch the news content
            soup=BeautifulSoup(resp_html.decode('utf-8','ignore'))
            struct_div=soup.find_all("div",attrs={"class": "river"})
            num=0
            for onenews in struct_div:
                num+=1
                news_temp=onenews.find("div",attrs={"class": "span4 river-image"})

                try:
                    news_url_temp=news_temp.find("a")
                    news_url=news_url_temp.get("href")
                    print news_url

                    image_url_temp=news_temp.find("img")
                    image_url=image_url_temp.get("src")
                    print image_url

                    time_temp=onenews.find("li",attrs={"class": "date"})
                    publish_time=time_temp.get_text()
                    print publish_time
                    
                except:
                    print "Error!"

if __name__=="__main__":
    main()
