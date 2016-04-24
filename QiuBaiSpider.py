# -*- coding=utf8 -*-

import urllib3
import urllib
import urllib.parse
import threading
import _thread
import re
import time


class QiuBaiSpider:
    def __init__(self):
        self.page = 1;
        self.pages = [];
        self.enable = False;
        self.base_url = "http://m.qiushibaike.com/hot/page/"
        self.http = urllib3.PoolManager()
        
        
    def get_page(self, page):
        url = self.base_url + str(page) + '/?s=4871432'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
        headers = { 'User-Agent' : user_agent }  
        resp = self.http.request('GET', url, headers=headers)
        b_content = resp.data
        content = b_content.decode("utf-8") 
        #print(content)
        items = re.findall('<div.*?class="content".*?title="(.*?)">(.*?)</div>', content, re.S)
        
        list = []    
        for item in items:
            print(item)
            list.append([item[0].replace("\n",""),item[1].replace("\n","")])    
        return list    

    def load_page(self):    
        while self.enable:    
            if len(self.pages) < 2:    
                try:       
                    myPage = self.get_page(str(self.page))    
                    self.page += 1    
                    self.pages.append(myPage)    
                except:    
                    print ('can\'t connect')
            else:    
                time.sleep(1)    
            
    def show_page(self,nowPage,page):    
        for items in nowPage:    
            print ( items[0]  , items[1]) 
            myInput = input()    
            if myInput == "quit":    
                self.enable = False    
                break    
            
    def start(self):    
        self.enable = True    
        page = self.page    
    
        print ("loading")  
            
       
        _thread.start_new_thread(self.load_page,())    
            
      
        while self.enable:    
            if self.pages:    
                nowPage = self.pages[0]    
                del self.pages[0]    
                self.show_page(nowPage,page)    
                page += 1    
    
    

myModel = QiuBaiSpider()    
myModel.get_page(1)    
