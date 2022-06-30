#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import re 
import pysolr
import requests 


# In[2]:


base_url = "https://kahaba.net/berita-kota-bima";

urlList = []
for i in range (1, 72):
    req = requests.get(base_url + "/page/" + str(i))
    soup = BeautifulSoup(req.text, "html.parser")
    for a in soup.find_all('a',href=True):
        url = a['href']
        if ((url[0:38] == "https://kahaba.net/berita-kota-bima/95")or(url[0:38] == "https://kahaba.net/berita-kota-bima/82")or(url[0:38] == "https://kahaba.net/berita-kota-bima/81")or(url[0:38] == "https://kahaba.net/berita-kota-bima/85")or(url[0:38] == "https://kahaba.net/berita-kota-bima/90")) :
#             print(url)
            urlList.append(url)


# In[3]:


print(len(urlList))
# print(urlList)


# In[4]:


result = [] 
for i in urlList: 
    if i not in result: 
        result.append(i) 


# In[5]:


print(len(result))
print(result[13])


# In[6]:


def scrap(url) : 
    req = requests.get(url)
    soup = BeautifulSoup(req.text,"html.parser")


    title = soup.title.text
       
    body = ""
    for p in soup.find_all('p') : 
        body += p.text
    
    if body == "" :
        body = " "
        for p in soup.find_all('p') : 
            body += p.text

    time = soup.time.text

    
    return {"id": url, "title_txt_id":title, "body_txt_id":body, "pdate" : time}


# In[7]:


data = []
for i in range(len(result)):
    data.append(scrap(result[i]))
#     print(data)
# #     print(result[i])



# In[8]:


print(len(data))


# In[9]:


print(data)


# In[10]:


import pysolr
solr = pysolr.Solr("http://localhost:8983/solr/core_uas/")
solr.ping()


# In[24]:


solr.delete(q="*:*")
solr.commit()


# In[11]:


solr.add(data)
solr.commit()


# In[ ]:




