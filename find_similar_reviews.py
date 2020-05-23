# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 23:24:45 2020

@author: megha
"""
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from helper_functions import *




str_val = "Cats love" #Input your string

df_reviews = pd.read_json("amazonReviews.json",lines=True)

df = pd.read_json("data.json",lines=True)

a=df['a'][0] 
b=df['b'][0]
m=df['m'][0] 
k=df['k'][0] 
stop_words=df['stop_words'][0]
my_ascii=df['my_ascii'][0] 
bucket_val=df['bucket_val'][0] 
li_a=df['li_a'][0] 
li_b=df['li_b'][0]
bands=df['bands'][0] 
r = df['r'][0] 
length = df['length'][0] 
length_big = df['length_big'][0] 
data = df['data'][0] 
x=df['x'][0]
y=df['y'][0] 

bin_rep = coo_matrix((data,(y,x)),shape=((len(my_ascii)**k),max(x)+1),dtype=np.bool)
bin_rep = bin_rep.tocsc()


index = get_similar_one(str_val,a,b,m,k,stop_words,my_ascii,bucket_val,li_a,li_b,bands,r,length,length_big,bin_rep)

df_csv=pd.DataFrame(columns=['Reviews similar to the given review([reviewerID,reviewText])'], index=range(len(index)))
i=0
for li in index:
     temp_text1=[]
 
     temp_text1.append(df_reviews['reviewerID'][li])
     temp_text1.append(df_reviews['reviewText'][li])

     df_csv['Reviews similar to the given review([reviewerID,reviewText])'].loc[i]=temp_text1
     i=i+1
df_csv.to_csv("matches_for_your_string.csv") 



