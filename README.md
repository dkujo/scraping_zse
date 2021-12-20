# Scraping Zagreb Stock Exchange (ZSE, www.zse.hr): Project Overview
This project enables comparison between different stock prices and index (Crobex) that measures stock market returns. ZSE website does not offer this feature. User can select two different stocks and compare their value during analysed time period. Web app is deployed using Streamlit. 
* using Selenium to scrape data from ZSE website
* extracting stock symbols and ISIN number
* extracting timeseries data and stock prices into Pandas dataframe
* extracting Crobex (market index) values into Pandas dataframe
* ploting and comparing extracted data
