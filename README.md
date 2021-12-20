# Scraping Zagreb Stock Exchange (ZSE, www.zse.hr): Project Overview
This project enables comparison between different stock prices and market index (Crobex) that measures stock market returns. ZSE website does not offer this feature directly. User  selects two different stocks while app returns their chart comparison during analysed time period together with Crobex index change. Web app is deployed using Streamlit. Project includes: 
* using Selenium to scrape data from ZSE website
* extracting stock symbols and stock ISIN number
* extracting timeseries data and stock prices into Pandas dataframe
* extracting Crobex (market index) values into Pandas dataframe
* ploting and comparing extracted data
* presenting results using Stremlit web app

## Code and Resources Used 
**Python Version:** 3.9.7 
**Packages:** pandas, selenium, altair, streamlit, time
**Selenium documentation**: https://www.selenium.dev/selenium/docs/api/py/api.html
