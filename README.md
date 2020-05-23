
# []()ESE545 Project1
##### []()File Structure:

1. 
    
    [Main.py](http://Main.py):It is the main python file which gives two outputs:  
    &#10;1.1) It finds all the pairs of similar review texts for a given JSON input file. The output is a CSV file containing filtered pairs of similar reviews. We have removed strings which are blank or consists of only stop words from the output. Output CSV is named as “results_106_6_5.csv”, where m=102 is the number of hash functions, r=6 is the number of rows in each band and k=5 is the length of each shingle. To check for different values of the number of hash functions, length of shingles and length of bands, hyperparameters m, k, r can be changed respectively which are specified at the beginning of the file.
    
    1.2) You may write your string to be tested for before hand in the main file in the variable “str_val” and in the end, the main code writes all the similar reviews to the given review in the “matches_for_your_string.csv” file. \
    
    Also, it may be noted that all the intermediate results from the previous steps can be stored in a .json file by uncommenting the code block from line 121 (savior) to line  153 (json dump). Note that this is going to be a huge file of about 900 MB. Comment all the code following this and you may then use “get_similar_reviews.py” file to find matches for your string by setting its str_val variable appropriately as explained in point 3. It shall save the results similarly as in 1.2. This may help save time when testing for multiple strings with minimal changes in the code since you do not have to run the whole code in the main file as the results are pre-computed and stored.


1. 
    
    helper [function.py](http://function.py): It has various helper python functions that are used in [main.py](http://main.py)


3)find_similar_reviews.py can be .py:  As explained above, it is another way for checking for similar reviews for a given string for Q6. For a given review text, it returns a CSV file named “matches_for_your_string.csv” which contains a list of reviewsTexts and reviewerId’s of matching strings. The input string to be tested is saved in the variable named “str_val”. Please note that the current value of the str_val is “Cats love”. This does similar task as that of commented code at the end of [main.py](http://main.py). This particular .py file can be used if desired to test for multiple strings on the fly as it doesn’t require running the complete [main.py](http://main.py) file. It can be further noted that this file needs a JSON file containing which has all the required parameters and hyperparameters saved after uncommenting the block explained in 1.2 and running the [main.py](http://main.py) at least once.
##### []()Steps to run the file:
Default settings:


1. Please keep the data  amazonReviews.json in the same directory as the code files.
1. Run [main.py](http://main.py) from any IDE of choice or command prompt. This will output 2 files:  
    
    i) results_12_6_5.csv having all the filtered pairs of similar reviews.  
    
    ii) matches_for_your_string.csv which contains a list of all similar reviews for a given input value in the variable “str_val” set to “Cats love” by default (maybe changed as desired).


Alternatively:  
&#10;Uncomment the code block from line  121 (savior) to line  153 (json dump) to get json file output of the intermediate results and use it to find similar reviews to a given string using “Find_similar_reviews.py” which then outputs “matches_for_your_string.csv”.
## []()Authors:

1. Saumya Shah
1. Megha Mishra


