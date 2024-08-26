# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 14:40:55 2024

@author: Sally.Pham
"""

#### Data Processing/Preparation and Exploratory Data Analysis (EDA) Script ####
# 1. Set-up
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

sns.set_palette("colorblind")

os.chdir('C:\\Users\\Sally.Pham\\OneDrive - insidemedia.net\\Documents\\Personal Development\\BPP University\\BSc Data Science 1.0\\Data Science Professional Practice\\0. Assignments\\Summative\\1. Data')

# 2a. Process Sephora Data
## read in product info and review files
product_info = pd.read_csv('1. Raw\\product_info.csv')

reviews_1 = pd.read_csv('1. Raw\\reviews_0-250.csv')
reviews_2 = pd.read_csv('1. Raw\\reviews_250-500.csv')
reviews_3 = pd.read_csv('1. Raw\\reviews_500-750.csv')
reviews_4 = pd.read_csv('1. Raw\\reviews_750-1250.csv')
reviews_5 = pd.read_csv('1. Raw\\reviews_1250-end.csv')

## merge review files
reviews = pd.concat([reviews_1, reviews_2, reviews_3, reviews_4, reviews_5])

## check for missing values and drop rows with missing values
missing_values_count = reviews.isnull().sum()
print(missing_values_count)

complete_reviews = reviews.dropna()

## check for duplicates and remove if any
duplicates_count = complete_reviews.duplicated().sum()
print(duplicates_count)

#complete_reviews = complete_reviews.drop_duplicates()
#commented out as there are no duplicates

## merge product info with rewiews dataframe by product_id
sephora_master = pd.merge(complete_reviews, product_info, on='product_id', how='inner')

## output sephora dataset to create a lookup that filters unwanted columns
#sephora_master.to_csv('2. Processed\\sephora_master.csv')

## read in lookup
lookup = pd.read_excel('0. Scripts\\sephora_lookup.xlsx')

## get columns to keep based on lookup and filter sephora master based on this
keep = lookup[lookup['filter'] == 'keep']['column'].values
sephora_final = sephora_master[keep]

## remove rows where secondary_category = Self Tanners, Value & Gift Sets, Wellness, High Tech Tools, Shop by Concern
remove = ['Self Tanners','Value & Gift Sets','Wellness','High Tech Tools','Shop by Concern']
sephora_final = sephora_final[~sephora_final['secondary_category'].isin(remove)]

## format
sephora_final = sephora_final.rename(columns = {
                'product_name_y': 'product_name',
                'brand_name_y': 'brand_name',
                'rating_y': 'rating',
                'price_usd_y': 'price_usd',
                'secondary_category': 'product_category'
                })

## enrich the dataset with new features / feature engineering
sephora_final['price_category'] = pd.cut(sephora_final['price_usd'], bins =[0,20,50,100,1000], labels=['low','medium','high','luxury'])
sephora_final['popularity_score'] = sephora_final['loves_count'] * sephora_final['rating']
# normalise the popularity score to get a value between 0 and 1 using min-max scaling
min_popularity = sephora_final['popularity_score'].min()
max_popularity = sephora_final['popularity_score'].max()
sephora_final['popularity_score_normalised'] = (sephora_final['popularity_score'] - min_popularity) / (max_popularity - min_popularity)
# drop the popularity_score column
sephora_final = sephora_final.drop(columns=['popularity_score'])

## create function to process text in highlights+ingredients columns
def preprocess_text(text):
    if not isinstance(text, str):
        return "remove" #if missing
    text = text.lower()  # lowercase
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    words = text.split()  # split
    words = [word for word in words if word not in ENGLISH_STOP_WORDS]  # remove stopwords
    return ' '.join(words)

## process text, drop original highlights column and remove missing rows
sephora_final['highlights_proc'] = sephora_final['highlights'].apply(preprocess_text)
sephora_final['ingredients_proc'] = sephora_final['ingredients'].apply(preprocess_text)

sephora_final = sephora_final.drop(columns=['highlights','ingredients'])
sephora_final = sephora_final[sephora_final['highlights_proc'] != 'remove']
sephora_final = sephora_final[sephora_final['ingredients_proc'] != 'remove']


# 2b. Explore Sephora Dataset / Further Processing
## check unique values for skin type, skin tone
sephora_final.skin_type.unique()
sephora_final.skin_tone.unique()

## remove rows that contain "notSureST" in skin tone column
sephora_final = sephora_final[sephora_final['skin_tone'] != 'notSureST']


## HISTOGRAMS/BOXPLOTS OF NUMERICAL VARIABLES
## distribution of product ratings
plt.figure(figsize=(10, 6))
sns.histplot(sephora_final['rating'], bins=10, kde=True)
plt.title('Distribution of Product Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

## distribution of price
plt.figure(figsize=(10, 6))
sns.histplot(sephora_final['price_usd'], bins=10, kde=True)
plt.title('Distribution of Price')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

## distribution of popularity score
plt.figure(figsize=(10, 6))
sns.boxplot(x='popularity_score_normalised', data=sephora_final, color=sns.color_palette("colorblind")[0])
plt.title('Box Plot of Popularity Scores')
plt.xlabel('Popularity Score')
plt.show()


## BAR CHARTS/PIE CHARTS OF CATEGORICAL VARIABLES
## distribution of skin type
plt.figure(figsize=(8, 8))
skin_type_counts = sephora_final['skin_type'].value_counts()
plt.pie(skin_type_counts, labels=skin_type_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Skin Type')
plt.show()

## distribution of skin tone
plt.figure(figsize=(8, 8))
skin_tone_counts = sephora_final['skin_tone'].value_counts()
plt.pie(skin_tone_counts, labels=skin_tone_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Skin Tone')
plt.show()

## distribution of eye colour
plt.figure(figsize=(8, 8))
eye_color_counts = sephora_final['eye_color'].value_counts()
plt.pie(eye_color_counts, labels=eye_color_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Eye Colour')
plt.show()

## distribution of hair colour
plt.figure(figsize=(8, 8))
hair_color_counts = sephora_final['hair_color'].value_counts()
plt.pie(hair_color_counts, labels=hair_color_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Hair Colour')
plt.show()

## distribution of products
plt.figure(figsize=(14, 8))
product_counts = sephora_final['product_name'].value_counts().head(10)  # top 10 reviewed products
sns.barplot(x=product_counts.values, y=product_counts.index)
plt.title('Top 10 Most Reviewed Products')
plt.xlabel('Count')
plt.ylabel('Product Name')
plt.show()

## distribution of brand names
plt.figure(figsize=(14, 8))
brand_counts = sephora_final['brand_name'].value_counts().head(10)  # top 10 reviewed brands
sns.barplot(x=brand_counts.values, y=brand_counts.index)
plt.title('Top 10 Most Reviewed Brands')
plt.xlabel('Count')
plt.ylabel('Brand Name')
plt.show()

## distribution of price category
plt.figure(figsize=(10, 6))
sns.countplot(x='price_category', data=sephora_final)
plt.title('Distribution of Price Category')
plt.xlabel('Price Category')
plt.ylabel('Count')
plt.show()

## distribution of product category
plt.figure(figsize=(8, 8))
product_category_counts = sephora_final['product_category'].value_counts()
plt.pie(product_category_counts, labels=product_category_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Product Category')
plt.show()


## OTHER CHARTS
## stacked bar chart for distribution of price within each product category
price_distribution = sephora_final.groupby(['product_category', 'price_category']).size().unstack() # group by 'product_category' and 'price_category', then count the instances

price_distribution.plot(kind='bar', stacked=True, figsize=(14, 8))
plt.title('Price Category Distribution Within Product Categories')
plt.xlabel('Product Category')
plt.ylabel('Number of Products')
plt.legend(title='Price Category')
plt.xticks(rotation=45)
plt.show()

## bar chart showing average popularity score of each product category
plt.figure(figsize=(14, 8))
category_popularity = sephora_final.groupby('product_category')['popularity_score_normalised'].mean().sort_values(ascending=False)
sns.barplot(x=category_popularity.values, y=category_popularity.index)
plt.title('Average Popularity Score Across Product Categories')
plt.xlabel('Average Popularity Score')
plt.ylabel('Product Category')
plt.show()

## bar chart showing the top 10 brands based on popularity
plt.figure(figsize=(14, 8))
brand_popularity = sephora_final.groupby('brand_name')['popularity_score_normalised'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=brand_popularity.values, y=brand_popularity.index)
plt.title('Top 10 Brands Based on Popularity Score')
plt.xlabel('Average Popularity Score')
plt.ylabel('Brand Name')
plt.show()

## bar cahrt showing the top 10 most expensive brands
plt.figure(figsize=(14, 8))
brand_price = sephora_final.groupby('brand_name')['price_usd'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=brand_price.values, y=brand_price.index)
plt.title('Top 10 Most Expensive Brands')
plt.xlabel('Average Price (USD)')
plt.ylabel('Brand Name')
plt.show()

## bar chart showing the top 10 most affordable brands
plt.figure(figsize=(14, 8))
brand_price = sephora_final.groupby('brand_name')['price_usd'].mean().sort_values(ascending=True).head(10)
sns.barplot(x=brand_price.values, y=brand_price.index)
plt.title('Top 10 Least Expensive Brands')
plt.xlabel('Average Price (USD)')
plt.ylabel('Brand Name')
plt.show()

## violin plot showing the rating distribution across price categories
plt.figure(figsize=(14, 8))
sns.violinplot(x='price_category', y='rating', data=sephora_final)
plt.title('Rating Distribution Across Price Categories')
plt.xlabel('Price Category')
plt.ylabel('Rating')
plt.show()

## stacked bar chart for distribution of skin types within each product category
skin_type_distribution = sephora_final.groupby(['product_category', 'skin_type']).size().unstack() # group by 'product_category' and 'skin_type', then count the instances

skin_type_distribution.plot(kind='bar', stacked=True, figsize=(14, 8))
plt.title('Skin Type Distribution Across Product Categories')
plt.xlabel('Product Category')
plt.ylabel('Number of Products')
plt.legend(title='Skin Type')
plt.xticks(rotation=45)
plt.show()


# 3a. Process Synthetic Data
## read in synthetic user data
user_data = pd.read_csv('1. Raw\\synthetic_user_data.csv')

## check for missing values - there shouldn't be any as I did not set this up in Mockaroo
missing_values_count = user_data.isnull().sum()
print(missing_values_count)

## check for duplicates and remove if any
duplicates_count = user_data.duplicated().sum()
print(duplicates_count)

#user_data = user_data.drop_duplicates()
#commented out as there are no duplicates

## remove age and gender columns as they do not capture real-world nuances and therefore is non-representative and skin tone as it will not be used for clustering and recommendation engine
userdata_final = user_data.drop(columns = ['age','gender','skin_tone'])


# 3b. Explore Synthetic Dataset

## distribution of primary skin concern
plt.figure(figsize=(10, 6))
sns.countplot(x='primary_skin_concern', data=userdata_final)
plt.title('Distribution of Skin Concerns')
plt.xlabel('Skin Concerns')
plt.ylabel('Count')
plt.show()

## distribution of skin type, skin tone
plt.figure(figsize=(8, 8))
skin_type_counts = userdata_final['skin_type'].value_counts()
plt.pie(skin_type_counts, labels=skin_type_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Skin Type')
plt.show()

plt.figure(figsize=(8, 8))
skin_tone_counts = userdata_final['skin_tone'].value_counts()
plt.pie(skin_tone_counts, labels=skin_tone_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Skin Tone')
plt.show()


# 4. Summary Statistics
#sephora_df_sum = sephora_final.describe()
#user_df_sum = userdata_final.describe()

#sephora_df_sum.to_csv('3. Results/EDA/sephora_df_summary_stats.csv')
#user_df_sum.to_csv('3. Results/EDA/user_df_summary_stats.csv')


# 5. Output final datasets for analysis

#sephora_final.to_csv('2. Processed\\sephora_final.csv')
#userdata_final.to_csv('2. Processed\\userdata_final.csv')












