# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:57:40 2024

@author: Sally.Pham
"""

#### Data Analysis Script ####
# 1. Set-up
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from kmodes.kmodes import KModes

os.chdir('C:\\Users\\Sally.Pham\\OneDrive - insidemedia.net\\Documents\\Personal Development\\BPP University\\BSc Data Science 1.0\\Data Science Professional Practice\\0. Assignments\\Summative\\1. Data')

## read in processed user data
user_df = pd.read_csv('2. Processed\\userdata_final.csv')

## remove unused columns
user_df.drop(user_df.columns[user_df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
user_df = user_df.drop(columns = ['user_id'])


# 2. K-modes Clustering
## elbow method to find optimal k value
cost = []

K = range(1,5)
for num_clusters in list(K):
    kmode = KModes(n_clusters=num_clusters, init = "random", n_init = 5, verbose=1)
    kmode.fit_predict(user_df)
    cost.append(kmode.cost_)
    
plt.plot(K, cost, 'bx-')
plt.xlabel('No. of clusters')
plt.ylabel('Cost')
plt.title('Elbow Method For Optimal k')
plt.show()
## elbow curve shows that optimal k = 3

## build a model with 3 clusters
kmode = KModes(n_clusters=3, init = "random", n_init = 5, verbose=1)
clusters = kmode.fit_predict(user_df)
clusters

## merge the array of cluster values with user_df
user_df.insert(0, "cluster", clusters, True)
user_df

# 3. Output user data with clusters

user_df.to_csv('3. Results\\K-modes Clustering\\user_df_clustered.csv')


# 4. Visualise
## split user_df based on cluster number
c1 = user_df[user_df['cluster'] == 0]
c2 = user_df[user_df['cluster'] == 1]
c3 = user_df[user_df['cluster'] == 2]

## Distribution in cluster 1
plt.figure(figsize=(10, 6))
sns.countplot(x='primary_skin_concern', data=c1)
plt.title('C1: Distribution of Skin Concerns')
plt.xlabel('Skin Concerns')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='skin_type', data=c1)
plt.title('C1: Distribution of Skin Types')
plt.xlabel('Skin Types')
plt.ylabel('Count')
plt.show()

## Distribution in cluster 2
plt.figure(figsize=(10, 6))
sns.countplot(x='primary_skin_concern', data=c2)
plt.title('C2: Distribution of Skin Concerns')
plt.xlabel('Skin Concerns')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='skin_type', data=c2)
plt.title('C2: Distribution of Skin Types')
plt.xlabel('Skin Types')
plt.ylabel('Count')
plt.show()

## Distribution in cluster 3
plt.figure(figsize=(10, 6))
sns.countplot(x='primary_skin_concern', data=c3)
plt.title('C3: Distribution of Skin Concerns')
plt.xlabel('Skin Concerns')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='skin_type', data=c3)
plt.title('C3: Distribution of Skin Types')
plt.xlabel('Skin Types')
plt.ylabel('Count')
plt.show()




























