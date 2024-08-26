# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 23:25:05 2024

@author: Sally.Pham
"""

#### Product Categorisation Script ####
# 1. Set-up
import pandas as pd
import os
import re
from collections import Counter

os.chdir('C:\\Users\\Sally.Pham\\OneDrive - insidemedia.net\\Documents\\Personal Development\\BPP University\\BSc Data Science 1.0\\Data Science Professional Practice\\0. Assignments\\Summative\\1. Data')

## read in datasets
sephora_df = pd.read_csv('2. Processed\\sephora_final.csv')

## remove unused columns
sephora_df.drop(sephora_df.columns[sephora_df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)


# 2. Product Categorisation
## create a dictionary to map skin concerns/types to keywords from the highlights column
skinconcern_keywords = {
    'acne': ['acne','blemish','spots','spot','clear','clean','pimple'],
    'aging': ['wrinkle','fine lines','anti-aging','age-defying','antiaging','age'],
    'dryness': ['dry','hydrate','moisturize','dehydrated','hyaluronic','hydrating'],
    'dullness': ['dull','brighten','radiance','radiant','glow','plump','plumping','glowing'],
    'dark spots': ['dark spots','hyperpigmentation','brighten','post-inflammatory','blemish','redness'],
    'pores': ['pores','reduce pores','tighten','firm','tight'],
    'wrinkles': ['wrinkles','reduce wrinkles','fine lines','anti-aging','antiaging']
    }

skintype_keywords = {
    'oily':['oil','oily','oily skin'],
    'dry':['dry','dry skin'],
    'combination':['combination','combo','combination skin',],
    'normal':['normal','normal skin']
    }

## create a function to match products to skin concerns
def match_concern(highlights_proc, skinconcern_keywords):
    matched_concerns = []
    for concern, keywords in skinconcern_keywords.items():
        if any(keyword in highlights_proc for keyword in keywords):
            matched_concerns.append(concern)
    return matched_concerns

## create a function to match products to skin types
def match_type(highlights_proc, skintype_keywords):
    matched_types = []
    for skintype, keywords in skintype_keywords.items():
        if any(keyword in highlights_proc for keyword in keywords):
            matched_types.append(skintype)
    return matched_types

## apply functions to sephora_df
sephora_df['skin_concern_addressed'] = sephora_df['highlights_proc'].apply(lambda x: match_concern(x, skinconcern_keywords))
sephora_df['skin_type_compatability'] = sephora_df['highlights_proc'].apply(lambda x: match_type(x, skintype_keywords))

## convert lists to tuples
sephora_df['skin_concern_addressed'] = sephora_df['skin_concern_addressed'].apply(tuple)
sephora_df['skin_type_compatability'] = sephora_df['skin_type_compatability'].apply(tuple)

## remove eye colour, hair colour etc. columns because they will not be used in the recommendation system
sephora_df = sephora_df.drop(['skin_tone','skin_type','hair_color','eye_color'], axis=1)

## remove duplicates
sephora_df = sephora_df.drop_duplicates()


# 3. Output
## output sephora_df for streamlit app script
#sephora_df.to_csv('3. Results\\Recommendation Engine\\sephora_df_for_app.csv')


















