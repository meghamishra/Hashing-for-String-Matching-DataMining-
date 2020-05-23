


#IMPORTS
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from helper_functions import *
import time #May be commented with all the other time related lines,
            # this is just to keep track of time for each step
import json #This is to dump the saved results to be used later for finding similar pairs for given string


if __name__ == '__main__':
    k = 5
    m = 102
    r=6

    t0 = time.time()
    
    # Reading DataFrame
    df = pd.read_json("amazonReviews.json",lines=True)
    df_take=df[['reviewerID','reviewText']]
    
    num_reviews = len(df_take)  
    
    #Defining stop words
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    # getting cleaned texts
    df_take['reviewText'] = df_take['reviewText'].apply(lambda x:remove_stop(x,stop_words))
      
    # Creating ascii list of all characters
    my_ascii={str(i):i for i in range(10)}
    alpha_dict={chr(i): i-97+10  for i in range(97,123)}
    my_ascii.update(alpha_dict)
    
    extra_dict={" ":36, "@": 37}
    my_ascii.update(extra_dict)


    #Defining variables to use it as global

   
    # intermediate output after applying hashing on shingles
    df_concat= df_take['reviewText'].apply(lambda ent: coo_entries(ent,k,my_ascii))
    t1 = time.time()
    print("Binary Matrix formed. Time(in seconds) : ",t1-t0)
    
    
    

    x=np.concatenate(np.asarray(df_concat[0]),axis=0)
    y=np.concatenate(np.asarray(df_concat[1]),axis=0)
    data=[1]*len(x)
    
    bin_rep = coo_matrix((data,(y,x)),shape=((len(my_ascii)**k),df_take.shape[0]),dtype=np.bool)
    bin_rep = bin_rep.tocsc()
    
    length=get_prime(len(my_ascii)**k)
    length_big=get_prime(10*len(my_ascii)**k)
    np.random.seed(0)
    #Taking random indices for question 3
    
#    random_numbers=np.random.randint(0,len(df_take),size=20000)
#    rand1 = random_numbers[:int(len(random_numbers)/2)]
#    rand2 = random_numbers[int(len(random_numbers)/2):]
        
#    tup, dist=get_jaccard_all(rand1,rand2,bin_rep)
    
    # Grtting hash parameters
    a,b = make_hash(m,len(df_take))
    t0 = time.time()
    print("Min hashing to get the signature matrix")
    Ys=get_reviews_values_from_bin_rep(num_reviews,bin_rep)

    
    M=min_hash(m,a,b,Ys,num_reviews,length)
    t1 = time.time()
    print("Min Hasing Done. Time(in seconds) : ", t1-t0)   
    bands=len(M)//r
    t0 = time.time()    
    print("Hashing the signature matrix and finding the similar pairs")
    index_sets,bucket_val,li_a,li_b=get_similar(a,b,r,bands,length_big,M,df_take)
    t1 = time.time()
    print("Hashing done, pairs found. Time(in seconds) : ", t1-t0)    
    
    t0 = time.time()
    print("Filtering the pairs to find the True Positives")
    FP,TP = findFPTP(index_sets,bin_rep)
    t1 = time.time()
    print("True positives found. Time(in seconds) : ", t1-t0)
    print("Number of True Positive pairs found including the empty reviews: ", len(TP))
    
    t0 = time.time()
    TP_nonzero = []
    for pair in TP:
      if len(df_take['reviewText'][pair[0]])!=0 and len(df_take['reviewText'][pair[1]])!=0:
        TP_nonzero.append(pair)
    t1 = time.time()
    print("Filtered the non-null reviews and saving to .csv file. Time (in seconds) = ",t1-t0)
    df_csv=pd.DataFrame(columns=['text1([reviewerID,reviewText])','text2([reviewerID,reviewText])'], index=range(len(TP_nonzero)))
   
    i=0
    
    for li in TP_nonzero:
         temp_text1=[]
         temp_text2=[]
     
         temp_text1.append(df['reviewerID'][li[0]])
         temp_text1.append(df['reviewText'][li[0]])
         temp_text2.append(df['reviewerID'][li[1]])
         temp_text2.append(df['reviewText'][li[1]])

         df_csv['text1([reviewerID,reviewText])'].loc[i]=temp_text1
         df_csv['text2([reviewerID,reviewText])'].loc[i]=temp_text2
         i=i+1
    df_csv.to_csv("results_{}_{}_{}.csv".format(m,r,k)) 




########################################################################################
#### Uncomment below portion to save the intermediate json output file
######################################################################################## 
    
#    savior = {}
#    savior['a'] = a
#    savior['b'] = b
#    savior['m'] = m
#    savior['k'] = k
#    savior['stop_words'] = stop_words
#    savior['my_ascii'] = my_ascii
#    savior['bucket_val'] = bucket_val
#    savior['li_a'] = li_a
#    savior['li_b'] = li_b
#    savior['bands'] = bands
#    savior['r'] = r
#    savior['length'] = length
#    savior['length_big'] = length_big
#    savior['data'] = data
#    savior['x'] = x
#    savior['y'] = y
    
# 
#    class NumpyEncoder(json.JSONEncoder):
#        def default(self, obj):
#            if isinstance(obj, np.ndarray):
#                return obj.tolist()
#            return json.JSONEncoder.default(self, obj)
#    
#    with open('data.json', 'w') as outfile:
#        json.dump(savior, outfile,cls = NumpyEncoder)    
    
    
########################################################################################
#### Uncomment below portion to get similar strings for any given input string #########
###############(It's already uncommented in the default setting)########################
########################################################################################   

     
    str_val="Cats love" #Input your string
    
    index= get_similar_one(str_val,a,b,m,k,stop_words,my_ascii,bucket_val,li_a,li_b,bands,r,length,length_big,bin_rep)
    df_csv=pd.DataFrame(columns=['Reviews similar to the given review([reviewerID,reviewText])'], index=range(len(index)))
    i=0
    for li in index:
         temp_text1=[]
     
         temp_text1.append(df['reviewerID'][li])
         temp_text1.append(df['reviewText'][li])
    
         df_csv['Reviews similar to the given review([reviewerID,reviewText])'].loc[i]=temp_text1
         i=i+1
    df_csv.to_csv("matches_for_your_string.csv") 
    
    
    