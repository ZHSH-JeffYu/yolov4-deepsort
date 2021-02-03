#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import sys


# In[2]:


ori_txt=pd.read_csv(sys.argv,sep=';', header=None)


# In[3]:


no_fps = ori_txt.drop(ori_txt[ori_txt[0].str.startswith("FPS")].index)[:-1]


# In[4]:


def check_ID(w):
    m=w
    try:
        m=re.search(r'(?<=ID: )(\d*)(?=,)', w).group(1)
    except:
        pass
    return m
def check_class(w):
    m=w
    try:
        m=re.search(r'(?<=Class: )(\w*)(?=,)', w).group(1)
    except:
        pass
    return m
def check_Frame(w):
    m=None
    try:
        m=re.search(r'(?<=#:\W{2})(\w*)', w).group(1)
    except:
        pass
    return m


# In[5]:


no_fps["ID"]=no_fps[0].map(check_ID) 
no_fps["category"]=no_fps[0].map(check_class) 
no_fps["frame"]=no_fps[0].map(check_Frame)
no_fps['frame'].fillna(method='ffill', inplace=True)


# In[55]:


df_clear = no_fps.drop(no_fps[no_fps['ID'].str.startswith("F")].index)
df_clear.drop(0,axis=1,inplace=True)
df_clear.index = range(1,len(df_clear) + 1)
df_clear["category_ID"]=df_clear["category"]+"："+df_clear["ID"]


# In[56]:


df_clear["frame"]=df_clear["frame"].astype('int')


# In[57]:


ans=''
for i in set(df_clear["category"]):
    mask=df_clear["category"]==i
    tmp=f"{i}：{len(set(df_clear[mask]['category_ID']))}"
    ans+=(tmp+"\n")


# In[10]:


with open("car_counting.txt","w") as f:
        f.write(ans)

