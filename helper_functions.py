
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix



x = []
y=[]
j=0
    
    
def stripPunc(strr):
    """Strips punctuation from list of words"""
    puncList = ["`","~","[","%","]","|","{","}","=","<",">","_","-","+","*","^",".",";",":","!","?","/","\\",",","#","@","$","&",")","(","\"","'"]
    for punc in puncList:
      strr = strr.replace(punc,'')
    return strr


def remove_stop(review,stop_words):
  """ Solves question 1: remove punctuations, stop words and returns cleaned sentences"""
  review = review.lower()
  review_wo_punc = stripPunc(review)
  review_split = review_wo_punc.split(" ")
  review_sw_removed = [i for i in review_split if i not in stop_words]
  review_wo_sw = " "
  review_wo_sw = review_wo_sw.join(review_sw_removed)
  return review_wo_sw


def shingle_index(shingle,my_ascii):
    """get index of each single using hashing"""
    li=list(shingle)
    li = li[::-1]
    x=sum([(my_ascii[li[i]]*((len(my_ascii))**i)) for i in range(len(li))])
    return x


def find_column(review,k,my_ascii):
  """get index of each single using hashing"""
  index=[]
  if len(review)<k:
    review = ("@"*(k-len(review)))+review
  for i in range(len(review)-k+1):
    index.append(shingle_index(review[i:i+k],my_ascii))
  return index


def coo_entries(review,k,my_ascii):
  """ returns x and y entries of sparse array where x is index and y is hashing value of shingles"""
 
  global x,y,j
  column = find_column(review,k,my_ascii)
  y = column
  x = ([j]*len(column))
  j=j+1
#  if j%10000 == 0:
#      print(j)
  return pd.Series([np.asarray(x),np.asarray(y)])


def get_prime(len_df):
    '''returns next biggest prime after the length of given dataset'''
    length=len_df+1
    flag=True
    flag2=True
    while(flag):
      for i in range(2,int(length/2)):
        if length%i==0:
          flag2=False
          break
        if flag2:
          flag=False
        else:
          length=length+1
          
    return length


def findUnion(arr1, arr2):
    """optimized code from geeksforgeeks to find union of two vectors"""
    m = len(arr1)
    n = len(arr2) 
    i,j = 0,0
    ans = []
    while i < m and j < n: 
        if arr1[i] < arr2[j]: 
            ans.append(arr1[i]) 
            i += 1
        elif arr2[j] < arr1[i]: 
            ans.append(arr2[j]) 
            j+= 1
        else: 
            ans.append(arr2[j]) 
            j += 1
            i += 1
  
    # Print remaining elements of the larger array 
    while i < m: 
        ans.append(arr1[i]) 
        i += 1
  
    while j < n: 
        ans.append(arr2[j]) 
        j += 1
    return len(ans)

def findIntersection(arr1, arr2): 
    
    """optimized code from geeksforgeeks to find intersection of two vectors"""
    
    m = len(arr1)
    n = len(arr2) 
    i,j = 0,0
    ans = []
    while i < m and j < n: 
        if arr1[i] < arr2[j]: 
            i += 1
        elif arr2[j] < arr1[i]: 
            j+= 1
        else: 
            ans.append(arr2[j]) 
            j += 1
            i += 1
    return len(ans)


def get_jaccard_all(rand1,rand2,bin_rep):
    tup=[]
    dist=[]
    for i in range(len(rand1)):
      v1=bin_rep.getcol(rand1[i]).nonzero()[0]
      v2=bin_rep.getcol(rand2[i]).nonzero()[0]        
      denom = findUnion(v1,v2)
      num = findIntersection(v1,v2) 
      js=num/denom   
      dist.append(js)    
      tup.append((rand1[i],rand2[i]))
      
    return tup, dist
      
 

def make_hash(r,df_take_len):
  a=[]
  b=[]
  for i in range(r):
    a.append(np.random.randint(0,df_take_len,1))
    b.append(np.random.randint(0,df_take_len,1))
  return a,b


def min_hash(m,a,b,Ys,num_reviews,length):
  np.random.seed(0)
  M = np.zeros((m,num_reviews))
  for i in range(m):
      temp= ((a[i]*Ys + b[i])%length)
      M[i,:] = [min(k) for k in temp]
  return M
  

def get_reviews_values_from_bin_rep(num_reviews,bin_rep):
    Ys = []
    for i in range(num_reviews):
      Ys.append(bin_rep.getcol(i).nonzero()[0])
    Ys = np.asarray(Ys)
    return Ys
    
 
def get_similar(a,b,r,bands,length,M,df_take):
    index_sets=[]
    li_a=[]
    li_b=[]
    buc_ret=[]
    for i in range(bands):
      a,b=make_hash(r,len(df_take))
      li_a.append(a)
      li_b.append(b)
      a=np.array(a)
      b=np.array(b)
      table=M[(i*r):(i+1)*r,]
      temp=np.zeros((r,M.shape[1]))
      for k in range(r):
        temp[k]=(a[k]*table[k,]+b[k])%length
      bucket_val=temp.sum(axis=0)
      buc_ret.append(bucket_val)
      index_sets.extend([np.argwhere(val==bucket_val).flatten() for val in np.unique(bucket_val) if len(np.argwhere(val==bucket_val))>1])
    
    return index_sets,buc_ret,li_a,li_b



def calcJS(ind1,ind2,bin_rep):
  v1=bin_rep.getcol(ind1).nonzero()[0]
  v2=bin_rep.getcol(ind2).nonzero()[0]
  denom = findUnion(v1,v2)
  num = findIntersection(v1,v2)
  js=num/denom  
  return js



def findFPTP(index_sets,bin_rep):
  FP = []
  TP = []
  interesting = []
  pair_num=0
  for pairs in index_sets:
    pair_num+=1
    for i in range(len(pairs)):  
      for j in range(len(pairs[i+1:])):
        js = calcJS(pairs[i],pairs[i+1+j],bin_rep)
        if js<0.8:
          FP.append((pairs[i],pairs[i+1+j]))
        else:
          TP.append((pairs[i],pairs[i+1+j]))
     
  return list(set(FP)),list(set(TP))


def print_reviews(pairlist):
  for pair in pairlist:
    if len(df['reviewText'][pair[0]])>1:
      print(pair[0],":",df['reviewText'][pair[0]])
      print(pair[1],":",df['reviewText'][pair[1]])
      print("-----------------------------------")
      
def get_FPTP_one(index_sets,bin_rep_one,bin_rep):
    TP = []
    FP = []
    v1 = bin_rep_one.getcol(0).nonzero()[0]
    for index in index_sets:
      v2=bin_rep.getcol(index).nonzero()[0]
      denom = findUnion(v1,v2)
      num = findIntersection(v1,v2)
      js=num/denom 
      if js>=0.8:
          TP.append(index)
      else:
          FP.append(index)
    return TP,FP



def get_similar_one(str_val,a,b,m,k,stop_words,my_ascii,buc_ret,li_a,li_b,bands,r,length,len_big,bin_rep):
    index_sets=[]
    to_comp=[]
    Ys = []
    cleaned=remove_stop(str_val,stop_words)
    
    column = find_column(cleaned,k,my_ascii)
    y = column
    x = ([0]*len(column))
    
    
#    df_concat= coo_entries(cleaned,k,my_ascii)
#    x=np.concatenate(np.asarray(df_concat[0]),axis=0)
#    y=np.concatenate(np.asarray(df_concat[1]),axis=0)
    data=[1]*len(x)
    
    bin_rep_one = coo_matrix((data,(y,x)),shape=((len(my_ascii)**k),1),dtype=np.bool)
    bin_rep_one = bin_rep_one.tocsc()
    
    Ys.append(bin_rep_one.getcol(0).nonzero()[0])
    Ys = np.asarray(Ys)
    M = np.zeros((m,1))
    
    for i in range(m):
      temp= ((a[i]*Ys + b[i])%length)
      M[i,:] = [min(k) for k in temp]
    

      
    for i in range(bands):
      a1,b1=li_a[i],li_b[i]
      a1=np.array(a1)
      b1=np.array(b1)
      table=M[(i*r):(i+1)*r,]
   
      temp=np.zeros((r,M.shape[1]))
      for kk in range(r):
        temp[kk]=(a1[kk]*table[kk,]+b1[kk])%len_big

      bucket_val_one=temp.sum(axis=0)
      curr_buc=buc_ret[i]
      
      if len(np.argwhere(curr_buc==bucket_val_one))>=1:
          index_sets.extend(np.argwhere(curr_buc==bucket_val_one).flatten())
    index_sets = list(set(index_sets)) 
#    TP = index_sets
    TP,FP = get_FPTP_one(index_sets,bin_rep_one,bin_rep)

    
    return TP
    
   