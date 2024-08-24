# Personalised Skincare Recommendation System 

## Executive Summary
### Business Challenge
The business challenge addressed was the lack of personalised skincare product recommendations, which often result in users buying products that do not adequately meet their needs. Many consumers face difficulties in finding suitable skincare products due to generic and one-size-fits-all recommendations. The hypothesis was that by leveraging user-specific data and clustering techniques, a recommendation engine could deliver more accurate and personalised skincare suggestions. This project, therefore, aimed to develop a personalised skincare recommendation app that caters to individual skin characteristics. At the heart of this app is a recommendation engine, designed with a structured logic workflow (see Figure 1) to provide tailored skincare suggestions.

### Methods - Data Collection
The following data was used:
(1)	[Sephora product review data from Kaggle](https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews)
(2)	Synthetic user data from Mockaroo
(3)	Real-time weather data from the OpenWeatherMap API

### Methods - Data Processing
Data processing involved quality checks, cleaning, merging, and feature engineering using Python. Exploratory Data Analysis (EDA) was conducted on the Sephora and synthetic user datasets to understand the underlying patterns.

### Methods - Data Analysis
K-modes clustering was applied to the synthetic user data to group users with similar skin characteristics (e.g., skin type and skin concern). The analysis was conducted using Python.

### Results
Three clusters were identified, each with unique profiles characterised by specific skin types (e.g., dry), concerns (e.g., aging), and preferred ingredients (e.g., retinol). These profiles guided the recommendation engine in filtering products, leading to the development of an app that offers personalised skincare recommendations.

### Conclusion
The app performs well but could benefit from integrating more environmental factors and regular updates to the clustering model. Future expansions should focus on incorporating additional data, such as products from other retailers, and refining the recommendation accuracy.

## 
