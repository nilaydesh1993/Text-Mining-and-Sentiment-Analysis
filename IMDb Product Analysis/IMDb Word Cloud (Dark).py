"""
Created on Mon May 11 10:32:20 2020
@author: DESHMUKH
"""
#pip install wordcloud
import numpy as np
import requests # Importing requests to extract content from a url
from bs4 import BeautifulSoup as bs # Beautifulsoup is for web scrapping...used to scrap specific content 
import re 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image # Form import Image
from urllib.parse import urljoin

# ============================================================================================================
# Business Problem - Extracting reviews of Dark web-series from Snapdeal and performing sentimental analysis.
# ============================================================================================================

movie = []
url = 'https://www.imdb.com/title/tt5753856/reviews?ref_=tt_ql_3'
res = requests.get(url)
soup = bs(res.text,"lxml")

main_content = urljoin(url,soup.select(".load-more-data")[0]['data-ajaxurl'])  ##extracting the link leading to the page containing everything available here
response = requests.get(main_content)
broth = bs(response.text,"lxml")

for item in broth.select(".review-container"):
    review = item.select(".text")[0].text
    movie.append(review)
    print("Review: {}\n\n".format(review))
    
# I Only able to extract 25 Reviews form IMDb. So performainn my further code on that only.

################################## - Data Preprocessing and Word cloud- ##################################

# Joinining all the reviews into single paragraph 
movies_rev_string = " ".join(movie)

# Removing unwanted symbols incase if exists
movies_rev_string = re.sub("[^A-Za-z" "]+"," ",movies_rev_string).lower()
movies_rev_string = re.sub("[0-9" "]+"," ",movies_rev_string)

# Seprating Words in reviews - Tokenization
movies_reviews_words = movies_rev_string.split(" ")

# stop_words = stopwords.words('english') - Inbulid library of stopword

# Opening Custom Build Stopword Dataset
with open("stopwords_en.txt","r") as sw: 
    stopwords = sw.read()

# Coverting them individual Words. 
stopwords = stopwords.split("\n")

# Comparing Review with Stopword and only taking word which is present not in Stopwords. 
movies_reviews_words1 = [w for w in movies_reviews_words if not w in stopwords]
movies_reviews_words1 = [w for w in movies_reviews_words1 if not w in ['show','dark','season','character','season']]  # Custom Words

# Joinining all the reviews into single paragraph 
movies_rev_string1 = " ".join(movies_reviews_words1)

# WordCloud can be performed on the string inputs.That is the reason we have combined,entire reviews into single paragraph.

# Wordcloud
wordcloud_mo = WordCloud(font_path='Cooper Regular.ttf',background_color='black',width=1800,height=1400,max_words=300,colormap='jet').generate(movies_rev_string1)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wordcloud_mo)
#wordcloud_mo.to_file("wordCloud.png") # Saving Cloud 

################################## - Sentimental Analysis Positive - ####################################

# Positive dataset words for postive sentiment
with open("positive-words.txt") as pos:
  poswords = pos.read().split("\n")

# Comparing Review with poswords and only taking word which is present in poswords. 
movies_pos_in_pos = " ".join ([w for w in movies_reviews_words if w in poswords])

# Positive Wordcloud 
wordcloud_mo_pos = WordCloud(font_path='Cooper Regular.ttf',background_color='black',width=1800,height=1400,max_words=300,colormap='RdBu',repeat=False).generate(movies_pos_in_pos)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wordcloud_mo_pos)
#wordcloud_mo_pos.to_file("po-wordCloud.png") # Saving Cloud 

################################## - Sentimental Analysis Negative - ####################################

# Negative dataset words for negative sentiment
with open("negative-words.txt") as pos:
  negwords = pos.read().split("\n")

# Comparing Review with negwords and only taking word which is present in negwords. 
movies_neg_in_neg = " ".join ([w for w in movies_reviews_words1 if w in negwords])

# Negative Wordcloud 
wordcloud_mo_neg = WordCloud(font_path='Cooper Regular.ttf',background_color='black',width=1800,height=1400,colormap='Greens',repeat=False).generate(movies_neg_in_neg)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wordcloud_mo_neg)
#wordcloud_mo_neg.to_file("neg-wordCloud.png") # Saving Cloud 

                             # ---------------------------------------------------- #






    
    
    
    
    
    
    
    
    