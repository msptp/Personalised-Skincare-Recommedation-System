# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 23:46:48 2024

@author: Sally.Pham
"""

#### Streamlit App Script ####
# 1. Set-up
import pandas as pd
import os
import requests
import streamlit as st
import matplotlib.pyplot as plt

os.chdir('C:\\Users\\Sally.Pham\\OneDrive - insidemedia.net\\Documents\\Personal Development\\BPP University\\BSc Data Science 1.0\\Data Science Professional Practice\\0. Assignments\\Summative\\1. Data')

## read in datasets
sephora_df = pd.read_csv('3. Results\\Skincare\\Recommendation Engine\\sephora_df_for_app.csv')
user_cluster_df = pd.read_csv('3. Results\\Skincare\\K-modes Clustering\\user_df_clustered.csv')

## clean
sephora_df.drop(sephora_df.columns[sephora_df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
user_cluster_df.drop(user_cluster_df.columns[user_cluster_df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
user_cluster_df = user_cluster_df.rename(columns={'primary_skin_concern': 'skin_concern'})

## define cluster profiles
cluster_profiles = {
    'Smooth Blend': {
        'skin_concerns': ['acne'],
        'skin_types': ['combination', 'normal'],
        'ingredients': ['salicylic acid', 'niacinamide', 'kaolin clay', 'sulfur', 'sulphur', 'benzoyl peroxide', 
                        'retinol', 'azelaic acid', 'hyaluronic acid', 'tea tree oil', 'green tea extract', 
                        'aloe vera', 'lactic acid', 'alpha-hydroxy acid', 'glycolic acid', 'adapalene', 
                        'vitamin c', 'ceramide']
    },
    'Balanced Skin': {
        'skin_concerns': ['dryness'],
        'skin_types': ['oily'],
        'ingredients': ['hyaluronic acid', 'ceramide', 'peptide', 'niacinamide', 'glycerin', 
                        'dimethicone', 'shea butter', 'urea', 'petrolatum', 'aloe vera', 
                        'squalene', 'beeswax', 'alpha-hydroxy acid', 'glycolic acid', 'lactic acid']
    },
    'Timeless Hydra': {
        'skin_concerns': ['aging'],
        'skin_types': ['dry'],
        'ingredients': ['retinol/vitamin a', 'vitamin c', 'vitamin e', 'superoxide dismutase', 
                        'beta-carotene', 'glutathione', 'selenium', 'green tea', 'soy extract', 
                        'grape extract', 'pomegranate extract', 'ceramide', 'lecithin', 'glycerin', 
                        'polysaccharide', 'hyaluronic acid', 'sodium pca', 'peptide', 'amino acid', 
                        'cholesterol', 'glycosaminoglycans', 'niacinamide', 'collagen']
    }
}



# 2. Functions

## checks for weather the user belongs to a cluster profile
def assign_user_to_cluster(user, cluster_profiles):
    for cluster, profile in cluster_profiles.items():
        if (user['skin_type'] in profile['skin_types'] and 
            user['skin_concern'] in profile['skin_concerns']):
            return cluster
    return None



## recommends best products for the user that belongs in the cluster profile based on popularity
def recommend_top_products_for_user(user, sephora_df, top_n=5):
    # Determine the user's cluster
    cluster = assign_user_to_cluster(user, cluster_profiles)
    
    # Get the cluster profile
    profile = cluster_profiles[cluster]
    
    # Extract user skin concerns and types
    skin_concern = user['skin_concern']
    skin_type = user['skin_type']
    
    # Extract ingredients from the cluster profile
    ingredients = profile['ingredients']
    
    # Filter products that include the skin concern
    concern_filter = sephora_df['skin_concern_addressed'].apply(lambda x: skin_concern in x)
    
    # Filter products that include the skin type
    type_filter = sephora_df['skin_type_compatability'].apply(lambda x: skin_type in x)
    
    # Filter products that include any of the ingredients
    ingredient_filter = sephora_df['ingredients_proc'].apply(lambda x: any(ingredient in x for ingredient in ingredients))
        
    # Combine filters
    filtered_products = sephora_df[concern_filter & type_filter & ingredient_filter]
    
    if filtered_products.empty:
        return pd.DataFrame()
    
    # Group by product category and get the top products by popularity score
    top_by_popularity = filtered_products.groupby('product_category').apply(
        lambda x: x.nlargest(top_n, 'popularity_score_normalised')
    ).reset_index(drop=True)
    
    return top_by_popularity



## recommends best products for the non-cluster users based on popularity
def recommend_top_products_for_non_cluster_user(user, sephora_df, top_n=5):
    skin_concern = user['skin_concern']
    skin_type = user['skin_type']
    
    # Filter products that include the skin concern
    concern_filter = sephora_df['skin_concern_addressed'].apply(lambda x: skin_concern in x)
    
    # Filter products that include the skin type
    type_filter = sephora_df['skin_type_compatability'].apply(lambda x: skin_type in x)
    
    # Combine filters
    filtered_products = sephora_df[concern_filter & type_filter]
    
    if filtered_products.empty:
        return pd.DataFrame()
    
    # Group by product category and get the top products by popularity score
    top_by_popularity = filtered_products.groupby('product_category').apply(
        lambda x: x.nlargest(top_n, 'popularity_score_normalised')
    ).reset_index(drop=True)
    
    return top_by_popularity



## gets current humidity levels
def get_weather(city, api_key):
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(weather_url)
    data = response.json()
    
    humidity = {
        'humidity': data['main']['humidity']
    }
    
    return humidity



## provides skincare recommendations/advice based on humidity levels
def get_humidity_advice(humidity):
    if humidity < 40:
        return "The current humidity level is low. Cleanse your face twice daily with a gentle cleanser. Follow up with a serum that has hyalauronic acid to promote hydration. Use a rich hydrating moisturiser with SPF."
    elif 40 <= humidity <= 60:
        return "The current humidity level is moderate. Maintain your usual skincare routine."
    else:
        return "The current humidity level is high. Cleanse your face twice daily with a gentle cleanser. Exfoliate to remove dead skin cells and prevent clogged pores. Use a lightweight or water-based SPF/moisturiser. Avoid oily products and heavy makeup."



def color_price_category(val):
    if val == 'Low':
        return 'background-color: #90EE90'  # Light green
    elif val == 'Medium':
        return 'background-color: #FFD700'  # Gold
    elif val == 'High':
        return 'background-color: #FFA07A'  # Light salmon
    return ''



def display_recommendations(df, title):
    if not df.empty:
        st.write(f"## {title}")
        # Select the columns we want to display, including price_usd
        display_df = df[['product_name', 'brand_name', 'price_category', 'price_usd', 'product_category', 'rating', 'popularity_score_normalised']]
        
        # Apply color styling
        styled_df = display_df.style.applymap(color_price_category, subset=['price_category'])
        
        st.dataframe(styled_df)

        # Iterate through each product category
        for category in display_df['product_category'].unique():
            category_df = display_df[display_df['product_category'] == category]
            
            st.write(f"### {category} - Top 5 Products")
            
            # Add a horizontal bar chart to visualize ratings
            st.write("#### Product Ratings")
            fig, ax = plt.subplots()
            ax.barh(category_df['product_name'], category_df['rating'])
            plt.xlim(0, 5)  # Assuming ratings are out of 5
            plt.tight_layout()
            st.pyplot(fig)
            
            # Add a scatter plot to compare price vs popularity with shorter product names
            st.write("#### Price vs Popularity 📉 ")
            fig, ax = plt.subplots()
            ax.scatter(category_df['price_usd'], category_df['popularity_score_normalised'])
            ax.set_xlabel('Price (USD)')
            ax.set_ylabel('Popularity Score')
            for i, txt in enumerate(category_df['product_name']):
                short_name = txt if len(txt) <= 20 else txt[:17] + '...'
                ax.annotate(short_name, (category_df['price_usd'].iloc[i], category_df['popularity_score_normalised'].iloc[i]))
            plt.tight_layout()
            st.pyplot(fig)
        
            # Add a scatter plot to compare price vs ratings with shorter product names
            st.write("#### Price vs Ratings 📈 ")
            fig, ax = plt.subplots()
            ax.scatter(category_df['price_usd'], category_df['rating'])
            ax.set_xlabel('Price (USD)')
            ax.set_ylabel('Rating')
            for i, txt in enumerate(category_df['product_name']):
                short_name = txt if len(txt) <= 20 else txt[:17] + '...'
                ax.annotate(short_name, (category_df['price_usd'].iloc[i], category_df['rating'].iloc[i]))
            plt.tight_layout()
            st.pyplot(fig)

        # Add a pie chart to visualize the distribution of price categories
        st.write("### Price Category Distribution 💵 ")
        price_counts = display_df['price_category'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(price_counts.values, labels=price_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
        
    else:
        st.write(f"No products found matching your criteria for {title.lower()}.")


# 3. Streamlit App

st.title("Personalised Skincare Recommendation System✨🧼🧴")
st.write(
    """
    Which skincare products are the right fit for you?
    
    This app helps you find the best skincare products tailored to your unique needs. Simply head to the left-hand side bar and follow the instructions to receive your recommendations.

    """
)

# User input
st.sidebar.header("Welcome! To get started, please: ")
skin_type = st.sidebar.selectbox("Select your skin type", ['normal', 'oily', 'combination', 'dry'])
skin_concern = st.sidebar.selectbox("Select your skin concern", ['dryness', 'dullness', 'wrinkles', 'acne','dark spots','aging','pores'])
city = st.sidebar.text_input("Enter your city")

user = {'skin_type': skin_type, 'skin_concern': skin_concern, 'city': city}

# Assign user to cluster
cluster = assign_user_to_cluster(user, cluster_profiles)
if cluster is not None:
    top_by_popularity = recommend_top_products_for_user(user, sephora_df)
else:
    top_by_popularity = recommend_top_products_for_non_cluster_user(user, sephora_df)

st.write(f"Your Skin Group = {cluster}")

display_recommendations(top_by_popularity, "Top Products by Popularity💓")

# Weather advice
if city:
    api_key = '7e07e61e6436837d28c4c0537154460f'
    weather = get_weather(city, api_key)
    if weather:
        humidity = weather['humidity']
        weather_advice = get_humidity_advice(humidity)
        st.write(f"## Weather Advice for {city}")
        st.write(weather_advice)
    else:
        st.write("Could not retrieve weather data")
else:
    st.write("🌤️ Enter a city to get weather-based skincare advice")