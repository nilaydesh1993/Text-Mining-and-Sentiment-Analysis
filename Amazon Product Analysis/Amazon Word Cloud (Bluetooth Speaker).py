"""
Created on Sun May 10 13:23:19 2020
@author: DESHMUKH
"""
#pip install wordcloud
import requests # Importing requests to extract content from a url
from bs4 import BeautifulSoup as bs # Beautifulsoup is for web scrapping...used to scrap specific content 
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# =================================================================================================
# Business Problem - Extracting reviews of Speaker from amazon and performing sentimental analysis.
# =================================================================================================

# Extracting Reviews of Speaker From Amazon 
speaker_reviews=[]                      
for i in range(1,50):  # For loop - start
  ip=[]  
  url="https://www.amazon.in/product-reviews/B07B2XRFRV/ref=acr_dpproductdetail_text?ie=UTF8&showViewpoints="+str(i)
  response = requests.get(url)
  soup = bs(response.content,"html.parser")# creating soup object to iterate over the extracted content 
#  reviews = soup.findAll("span",attrs={"class","a-size-base review-text review-text-content"}) # Extracting the content under specific tags  
  reviews = soup.findAll("span",{"data-hook":"review-body"})
  for i in range(len(reviews)):
    ip.append(reviews[i].text)  
  speaker_reviews=speaker_reviews+ip  # Adding the reviews of one page to empty list which in future contains all the reviews

# Writing reviews in a text file 
with open("speaker.txt","w",encoding='utf8') as output:
    for i in speaker_reviews:
        output.write(i+"\n")

import os
os.getcwd()

################################## - Data Preprocessing and Word cloud- ##################################

# For open saved Dataset or Existing Dataset
#with open("C:/Users/manik_ntfw8jz/speaker.tx","r",encoding='utf8') as sw:
#    iphone_reviews = sw.read()


# Joinining all the reviews into single paragraph 
speaker_rev_string = " ".join(speaker_reviews)

# Removing unwanted symbols incase if exists
speaker_rev_string = re.sub("[^A-Za-z" "]+"," ",speaker_rev_string).lower()
speaker_rev_string = re.sub("[0-9" "]+"," ",speaker_rev_string)

# Seprating Words in reviews - Tokenization
speaker_reviews_words = speaker_rev_string.split(" ")

# stop_words = stopwords.words('english') - Inbulid library of stopword

# Opening Custom Build Stopword Dataset
with open("stopwords_en.txt","r") as sw: 
    stopwords = sw.read()

# Coverting them individual Words. 
stopwords = stopwords.split("\n")

# Comparing Review with Stopword and only taking word which is present not in Stopwords. 
speaker_reviews_words1 = [w for w in speaker_reviews_words if not w in stopwords]

# Joinining all the reviews into single paragraph 
speaker_rev_string1 = " ".join(speaker_reviews_words1)

# WordCloud can be performed on the string inputs.That is the reason we have combined,entire reviews into single paragraph.

# Wordcloud
wordcloud_sp = WordCloud(font_path='Cooper Regular.ttf' ,background_color='black',width=1800,height=1400,max_words=300,colormap='tab20b').generate(speaker_rev_string1)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wordcloud_sp)
#wordcloud_sp.to_file("wordCloud.png") # Saving Cloud 

################################## - Sentimental Analysis Positive - ####################################

# Positive dataset words for postive sentiment
with open("positive-words.txt") as pos:
  poswords = pos.read().split("\n")

# Comparing Review with poswords and only taking word which is present in poswords. 
speaker_pos_in_pos = " ".join ([w for w in speaker_reviews_words if w in poswords])

# Positive Wordcloud 
wordcloud_sp_pos = WordCloud(font_path='Cooper Regular.ttf',background_color='black',width=1800,height=1400,max_words=300,colormap='RdBu',repeat=False).generate(speaker_pos_in_pos)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wordcloud_sp_pos)
#wordcloud_sp_pos.to_file("positive_wordCloud.png") # Saving Cloud 

################################## - Sentimental Analysis Negative - ####################################

# Negative dataset words for negative sentiment
with open("negative-words.txt") as pos:
  negwords = pos.read().split("\n")

# Comparing Review with negwords and only taking word which is present in negwords. 
speaker_neg_in_neg = " ".join ([w for w in speaker_reviews_words if w in negwords])

# Negative Wordcloud 
wordcloud_sp_neg = WordCloud(font_path='Cooper Regular.ttf',background_color='black',width=1800,height=1400,colormap='RdBu',repeat=False).generate(speaker_neg_in_neg)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wordcloud_sp_neg)
#wordcloud_sp_neg.to_file("negative_wordCloud.png") # Saving Cloud 

#Way for using personal words 
#temp = ["this","is","awsome","to","learn","Data","Science"]
#[i for i in temp if i not in "is"]

                             # ---------------------------------------------------- #





