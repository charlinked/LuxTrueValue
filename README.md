# LuxTrueValue

LuxTrueValue is a web app that provides smart pricing for luxury bags. LuxTrueValue was developed to empower bag lovers that buy and sell in resale, using platforms such as EBay, Poshmark and Mercari.

## 1. Motivation

Luxury resale has gained tremendous popularity, with many customers now buying and selling pre-owned luxury on e-commerce platforms such as EBay, Poshmark and Tradesy. When selling an item on these platforms, the seller determines the right asking price, and this can be very tricky for luxury items since no tools are available that accurately estimate market value. Items that are offered for sale under-value, or over-value (these often don't sell), cause both the sellers *and* the market place to miss out on profit. LuxTrueValue solves this problem for luxury bags: by inputting the specifics of a bag (color, style, brand, material,...), LuxTrueValue provides an accurate market value estimation in real time - in only a couple of clicks!

## 2. Website (http://drivenbydata.me)

![Image of homepage](https://github.com/charlinked/LuxTrueValue/blob/master/figures/homepage.png)

### how to interact with the Website
Different fields allow for the input of products specifics. To guide the user, infographics for different input fields were added.

![Image of selectionboxes](https://github.com/charlinked/LuxTrueValue/blob/master/figures/selectionboxes.png)

### output

The app outputs the market value at the bottom of the page in *real time*. The user can also play around with the product specifics and see how altering one feature influences the market value estimation: eg to know if buying a bag in a certain material is a better 'investment' when planning to resell that bag later on?)

![Image of output](https://github.com/charlinked/LuxTrueValue/blob/master/figures/output.png)

## 3. Pipeline

![Image of pipeline](https://github.com/charlinked/LuxTrueValue/blob/master/figures/pipeline.png)

Data was scraped using Beautiful Soup in Python. Raw data was loaded into Google BigQuery SQL database for data cleaning and feature engineering, after it was uploaded into a jupyter notebook and processed further with Pandas. Exploratory data analysis was done with Pandas, Numpy, Matplotlib and Seaborn.

An XGBoost model was trained on the total dataset - hyper-parameter tuning was done using a Gridsearch and cross-validation with the Mean Absolute Error (MAE) as metric for model performance.

To get an insight into feature importance I used both the eli5 and shap libraries. Eli5 allows for the computation of permutation importance, which is generally a better measure of feature importance than XGBoost's own feature importance module. The shap library can provide shapley values for individual predictions, that demonstrate how model the model outputs a certain value and what features are the biggest driver in that prediction.

### Data Sources

Data was scraped from different company websites that sell pre-owned luxury bags (Fashionphile, Rebag and Amore), I used BeautifulSoup in Python and a webdriver to scrape dynamic webpages.

### Data processing

Raw data was imported into Google BigQuery for data cleaning and feature engineering, a next layer of data cleaning was done in Pandas, where I also merged different tables.

### Building a prediction model

To build a prediction model I used XGBoost (Gradient boosting). XGBoost has a number of advantages that are important in this situation:
- Can model non-linear relationships
- Can deal with correlated and irrelevant features
- Typically outperforms a random forrest if well-tuined to prevent it from overfitting
- Suitable for medium-sized data sets

I evaluated my model using the mean absolute error (MAE) and Mean Absolute Percentage Error (MAPE). My final model has an accuracy of about 80% (measured by the MAPE)

### Designing a user interface

To design a user interface I worked with [streamlit](https://www.streamlit.io), a nifty tool that easily transform a machine learning model to a performant web app. Deployment of my streamlit app was done through an AWS EC2 instance.

## 4. LuxTrueValue, What's next?

With the rise of online resale, correct estimation of market value is key! - LuxTrueValue could easily be scaled to include many other products (think shoes, clothes,...!) and provide a market value estimation. 

Prefer to listen? Watch me demo LuxTrueValue in [this](https://www.youtube.com/watch?v=G4gp2c0PrRU) 5 minute YouTube video.

LuxTrueValue is a project for [Insight Data Science](https://insightfellows.com/data-science)
