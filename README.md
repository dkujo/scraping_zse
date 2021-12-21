# Scraping Zagreb Stock Exchange (ZSE, www.zse.hr): Project Overview
This app enables comparison between different stock prices and market index (Crobex) that measures stock market returns. ZSE website does not offer this feature directly. User  selects two different stocks while app returns their chart comparison during analysed time period together with Crobex index change. Web app is deployed using Streamlit. Project includes: 
* using Selenium to scrape data from ZSE website
* extracting all available stock symbols and stock ISIN number
* extracting timeseries data and selected stock prices into Pandas dataframe
* extracting Crobex (market index) values into Pandas dataframe
* ploting and comparing extracted data using basic Altair visualization
* choosing stocks and presenting results using Stremlit web app

## Code and Resources Used 
**Python Version:** 3.9.7

**Packages:** pandas, selenium, altair, streamlit, time

**Selenium documentation**: https://www.selenium.dev/selenium/docs/api/py/api.html

**Streamlit documentation**: https://docs.streamlit.io/

**Altair documentation**: https://altair-viz.github.io/

## Web Scraping
It is necessary to use Selenium as web-scaper because ZSE website is dynamic website (Beautifulsoup scraper is not appropiate).
Download browser driver that Selenium uses before scraping. For Chrome users: https://chromedriver.chromium.org/downloads. Check your Chrome version before download (Help --> About Google Chrome).

## Data presentation
Tablular data is shown as Pandas dataframe: 


Individual stock price chart is ploted as line graph:


Stock prices and Crobex comparison is ploted as multiple line graph:
