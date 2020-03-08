#!/usr/bin/env python
# coding: utf-8

# # Importing

# In[1]:


import requests
import csv
import json
from bs4 import BeautifulSoup


# # Web Scrapping

# In[2]:


page = 1
i = 0
final = []
while (page<=6):
    url = "https://www.zomato.com/bangalore/south-bangalore-restaurants?page="+str(page)
    page =page+1
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    response = requests.get(url,headers=headers)
    content = response.content
    soup = BeautifulSoup(content,"html.parser")
    res_type_containers = soup.findAll("div",{"class","col-s-12"})
    vote_rate_containers = soup.findAll("div",{"class","ta-right floating search_result_rating col-s-4 clearfix"})   
    for row in range(len(res_type_containers)):
        text = ''
        if(i==80):
            break
        else:
            restaurant_id = i + 1 
            text = res_type_containers[row].text
            text = text.strip()
            text = text.split('\n')
            name = text[1]
            area = text[-1]
            restaurant_type = text[0]
            rating = vote_rate_containers[0].div.text
            rating = " ".join(rating.split()) 
            vote = vote_rate_containers[0].span.text
            vote = " ".join(vote.split())
            local_dict = {
                "restaurant_id":restaurant_id,
                "name":name,
                "area":area,
                "restaurant_type":restaurant_type,
                "rating":rating,
                "votes":vote
                }
            final.append(local_dict)
            i=i+1


# # CSV Export

# In[3]:


csv_columns = ['restaurant_id','name','area','restaurant_type','rating','votes']
try:
    with open('output.csv', 'w',encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in final:
            writer.writerow(data)
except IOError:
    print("I/O error")


# # JSON Export

# In[4]:


json_object = json.dumps(final, indent = 6) 
  
# Writing to sample.json 
with open("output.json", "w") as outfile: 
    outfile.write(json_object) 

