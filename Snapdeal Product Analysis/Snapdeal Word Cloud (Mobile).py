"""
Created on Sun May 10 20:24:01 2020
by - Deshmukh
"""
#pip install wordcloud
import numpy as np
import requests # Importing requests to extract content from a url
from bs4 import BeautifulSoup as bs # Beautifulsoup is for web scrapping...used to scrap specific content 
import re 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image,ImageOps # Form import Image

# ===================================================================================================
# Business Problem - Extracting reviews of Mobile from Snapdeal and performing sentimental analysis.
# ===================================================================================================

# Extracting Reviews of Mobile From Snapdeal
mobile_snapdeal=[]
url1 = "https://www.snapdeal.com/product/xolo-era-2-8gb-black/639365186960/reviews?page="
url2 = "&sortBy=RECENCY#defRevPDP"                             
for i in range(1,60):
  mo=[]  
  base_url = url1+str(i)+url2
  response = requests.get(base_url)
  soup = bs(response.content,"html.parser")# Creating soup object to iterate over the extracted content 
  temp = soup.findAll("div",attrs={"class","user-review"})# Extracting the content under specific tags  
  for j in range(len(temp)):
    mo.append(temp[j].find("p").text)
  mobile_snapdeal=mobile_snapdeal+mo  # Adding the reviews of one page to empty list which in future contains all the reviews

# Removing repeated reviews 
mobile_snapdeal = list(set(mobile_snapdeal))

# Writing reviews into text file 
with open("mo_snapdeal.txt","w",encoding="utf-8") as snp:
    snp.write(str(mobile_snapdeal))
    
import os
os.getcwd()

################################## - Data Preprocessing and Word cloud- ##################################

# For open saved Dataset or Existing Dataset
#with open("C:/Users/manik_ntfw8jz/mo_snapdeal.txt","r",encoding='utf8') as sw:
#    iphone_reviews = sw.read()

# Joinining all the reviews into single paragraph 
mobile_rev_string = " ".join(mobile_snapdeal)

# Removing unwanted symbols incase if exists
mobile_rev_string = re.sub("[^A-Za-z" "]+"," ",mobile_rev_string).lower()
mobile_rev_string = re.sub("[0-9" "]+"," ",mobile_rev_string)  
    
# Seprating Words in reviews - Tokenization
mobile_reviews_words = mobile_rev_string.split(" ")    

# Opening Custom Build Stopword Dataset
with open("stopwords_en.txt","r") as sw: 
    stopwords = sw.read()    
    
# Coverting them individual Words. 
stopwords = stopwords.split("\n")

# Comparing Review with Stopword and only taking word which is present not in Stopwords. 
mobile_reviews_words1 = [w for w in mobile_reviews_words if not w in stopwords]
mobile_reviews_words1 = [w for w in mobile_reviews_words1 if not w in ['mobile','phone','cell','product','snapdeal']] # Some additional Words

# Joinining all the reviews into single paragraph 
mobile_rev_string1 = " ".join(mobile_reviews_words1)   
    
# WordCloud can be performed on the string inputs.That is the reason we have combined,entire reviews into single paragraph.

## Word Cloud 
wordcloud_sp = WordCloud(font_path='Friendly.otf',background_color='black',width=1800,height=1400,max_words=500,colormap='Blues',min_font_size=1).generate(mobile_rev_string1)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wordcloud_sp)
#wordcloud_sp.to_file("wordCloud.png") # Saving Cloud 

################################## - Sentimental Analysis Positive - ####################################

# Positive dataset words for postive sentiment
with open("positive-words.txt") as pos:
  poswords = pos.read().split("\n")

# Comparing Review with poswords and only taking word which is present in poswords. 
mobile_pos_in_pos = " ".join ([w for w in mobile_reviews_words if w in poswords])

# Positive Wordcloud 
wordcloud_mo_pos = WordCloud(font_path='Friendly.otf',background_color='black',width=1800,height=1400,max_words=1000,colormap='jet').generate(mobile_pos_in_pos)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wordcloud_mo_pos)  
#wordcloud_mo_pos.to_file("po-wordCloud.png") # Saving Cloud 

################################## - Sentimental Analysis Negative - ####################################

# Negative dataset words for negative sentiment
with open("negative-words.txt") as pos:
  negwords = pos.read().split("\n")

# Comparing Review with negwords and only taking word which is present in negwords. 
mobile_neg_in_neg = " ".join ([w for w in mobile_reviews_words if w in negwords])

# Modeified Wordcloud using image for shape.
## Load image. This has been modified in gimp to be brighter and have more saturation.
maskArray = np.array(Image.open("R.png").convert('RGB'))

# Negative Wordcloud 
wordcloud_sp_neg = WordCloud(font_path='Friendly.otf',mask=maskArray,background_color='black',width=1800,height=1400,colormap='magma').generate(mobile_neg_in_neg)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wordcloud_sp_neg)
#wordcloud_sp_neg.to_file("neg-wordCloud.png") # Saving Cloud 
 
                         # ---------------------------------------------------- #
    
    
    
    
