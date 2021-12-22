import pandas as pd
import streamlit as st
from datetime import datetime
from selenium import webdriver
import altair as alt
import time

########################### HELPER FUNCTIONS ###########################

def scrape_stock_symbols(driver_stock, url_stocks_symbols):

    driver_stock.get(url_stocks_symbols)
    time.sleep(1)
    #print(driver_stock.page_source) # check HTML content
    
    # use Pandas to scrape website tables
    stock_symbols = []
    stock_ISIN = []
    for df in pd.read_html(driver_stock.page_source, thousands='.', decimal='.'):
        # indentify desired table (use column names)
        if df.columns[1] == 'Simbol' and df.columns[2] == 'ISIN':
            #print(df['Simbol'])
            stock_symbols.extend(df['Simbol'])
            stock_ISIN.extend(df['ISIN'])
    
    stock_symbols = [x for x in stock_symbols if len(x)<=5] # filtering unnecessary scraped data
    stock_ISIN = [x for x in stock_ISIN if len(x)<=12]
    
    df_stocks_ISIN = pd.DataFrame(list(zip(stock_symbols, stock_ISIN)), columns =['Symbol', 'ISIN'])
    df_stocks_ISIN = df_stocks_ISIN.sort_values('Symbol').reset_index(drop=True)
    #df_stocks_ISIN
    
    df_stocks_ISIN['merged'] = df_stocks_ISIN['Symbol'] + '   ' + df_stocks_ISIN['ISIN']
    
    # write scraped data into csv file
    #df_stocks_ISIN['merged'].to_csv('stocks_symbols_and_ISIN.csv', index=False)
    
    return df_stocks_ISIN['merged'] 


def scrape_history(driver_stock, url):

    driver_stock.get(url)
    time.sleep(1)
    #print(driver_stock.page_source) # check HTML content

    # use Pandas to scrape website tables
    for df in pd.read_html(driver_stock.page_source, thousands='.', decimal='.'):
        # indentify desired table (use column names)
        if df.columns[0] == 'Datum' and df.columns[1] == 'Model':
            df_his = df # this is stock-history table
        elif df.columns[0] == 'Datum' and df.columns[1] == 'Prva':
            df_his = df   # this is crobex-history table
        else: df_his = 'HISTORY TABLE NOT FOUND'
    
    return df_his


def extract_data_from_df(dates,values):

    x=[]
    for date in dates[::-1]: # iterate date in reverse order
        #print(date)
        if len(str(date))==7:
            #print(date)
            date = '0'+ str(date)
            date = pd.to_datetime(date, format='%d%m%Y')
        else: date = pd.to_datetime(date, format='%d%m%Y')
        x.append(date)

    y=[]
    for value in values[::-1]:
        value=float(str(value).replace('.', '').replace(',','.'))
        #print(y)
        y.append(value)   
        
    return x, y

#################################################################################


#################### scrape stock symbols and ISIN from ZSE ####################
url_stocks_symbols = 'https://zse.hr/hr/cijene-vrijednosnih-papira/36?date=2021-11-29&model=CT&type=SHARE'

# specify path to chromedriver.exe (download and save on your computer before)
option = webdriver.ChromeOptions()
option.add_argument('headless') # prevent browser from opening
driver_stock = webdriver.Chrome(options=option)

stock_tickers_and_ISIN = scrape_stock_symbols(driver_stock, url_stocks_symbols)


#################### Streamlit title ####################
st.title('Scraping ZSE data')
st.markdown('This application scrapes stocks data from ZSE website, shows it as a table (Pandas dataframe), and displays it as a chart. Visit the ZSE website for more information: [link](https://zse.hr)')

# sidebar user input
st.sidebar.header('User Input')

# user selects two stocks for comparison
select_stock = st.sidebar.selectbox('Select first stock label and ISIN', stock_tickers_and_ISIN)
print(select_stock)
select_stock2 = st.sidebar.selectbox('Select second stock label and ISIN', stock_tickers_and_ISIN[1:])
print(select_stock2)

# user selects number of years to analyse
no_years = st.sidebar.slider('Number of years to analyse', 1, 5, 3)


################### stock price history range ###################
now = datetime.now()  # current date and time
today_date = now.strftime("%Y-%m-%d")

history_date = str(int(today_date[:4])-no_years)+today_date[4:]


################### select stocks ISIN to analyse ###################
start=select_stock.find('HR')
stock_ISIN=select_stock[start:]

start2=select_stock2.find('HR')
stock_ISIN2=select_stock2[start:]


# stock webpage URL (modified by 2 variables)
url_stock_history = 'https://zse.hr/hr/papir/310?isin=' + stock_ISIN + \
    '&tab=security_history&date_from=' + history_date + \
    '&date_to=' + today_date + '&model=ALL'

# call scraping function 
stock_history_data = scrape_history(driver_stock, url_stock_history)

# stock2 webpage URL (modified by 2 variables)
url_stock_history2 = 'https://zse.hr/hr/papir/310?isin=' + stock_ISIN2 + \
    '&tab=security_history&date_from=' + history_date + \
    '&date_to=' + today_date + '&model=ALL'
# call scraping function 
stock_history_data2 = scrape_history(driver_stock, url_stock_history2)


# extract time and price from stock history data
stock_time, stock_price = extract_data_from_df(stock_history_data['Datum'],stock_history_data['Zadnja'])
stock_history_data['Datum'] = [x.strftime('%Y-%m-%d') for x in stock_time][::-1]

# extract time and price from stock2 history data
stock_time2, stock_price2 = extract_data_from_df(stock_history_data2['Datum'],stock_history_data2['Zadnja'])
stock_history_data2['Datum'] = [x.strftime('%Y-%m-%d') for x in stock_time2][::-1]


# display stock history table on streamlit
st.write('### First stock history data table')
st.dataframe(stock_history_data)

dic_stock = {'Date':stock_time, str(select_stock):stock_price}
stock_plot=pd.DataFrame(data=dic_stock)
stock_plot.set_index('Date', inplace=True)

# plot stock history table on streamlit
st.write('### First stock history price chart')
st.line_chart(pd.DataFrame(stock_plot))


# display second stock history table on streamlit
st.write('### Second stock history data table')
st.dataframe(stock_history_data2)

dic_stock2 = {'Date':stock_time2, str(select_stock2):stock_price2}
stock_plot2=pd.DataFrame(data=dic_stock2)
stock_plot2.set_index('Date', inplace=True)

# plot stock history table on streamlit
st.write('### Second stock history price chart')
st.line_chart(pd.DataFrame(stock_plot2))


################### scraping crobex data - for comparing stocks and market returns ###################
url_crobex_history = 'https://zse.hr/hr/indeks/365?isin=HRZB00ICBEX6&tab=index_history&date_from=' + history_date + '&date_to=' + today_date

# call scraping function
crobex_history_data = scrape_history(driver_stock, url_crobex_history)

# extract time and price from crobex history data
crobex_time, crobex_value = extract_data_from_df(crobex_history_data['Datum'],crobex_history_data['Zadnja'])

# display Crobex history table on streamlit
st.write('### Crobex history data table')
st.dataframe(crobex_history_data)


dic_index = {'Date':crobex_time, 'Crobex_value':crobex_value}
crobex_plot=pd.DataFrame(data=dic_index)
crobex_plot.set_index('Date', inplace=True)

# plot crobex history table on streamlit
st.write('### Crobex history value chart')
st.line_chart(pd.DataFrame(crobex_plot))


st.write('### Stock prices and crobex value')
#find common dates for stock and crobex
common_time = list(set(stock_time).intersection(set(crobex_time)).intersection(set(stock_time2)))

# find crobex value at common time, remove duplicates (if any)
crobex_date_value = crobex_plot[crobex_plot.index.isin(common_time)]
crobex_date_value = crobex_date_value[~crobex_date_value.index.duplicated(keep='first')]

# find stock values at common time, remove duplicates (if any)
stock_date_price = stock_plot[stock_plot.index.isin(common_time)]
stock_date_price = stock_date_price[~stock_date_price.index.duplicated(keep='first')]

# find stock2 values at common time, remove duplicates (if any)
stock_date_price2 = stock_plot2[stock_plot2.index.isin(common_time)]
stock_date_price2 = stock_date_price2[~stock_date_price2.index.duplicated(keep='first')]

# join stock and crobex data into new dataframe
stock_index_data = pd.concat([stock_date_price,stock_date_price2[str(select_stock2)],crobex_date_value.Crobex_value], axis=1)

# create interactive chart on streamlit app
source = stock_index_data.reset_index().melt('Date', var_name='Category', value_name='Value')

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Date'], empty='none')

# The basic line
line = alt.Chart(source).mark_line(interpolate='basis').encode(
    x='Date:T',
    y='Value:Q',
    color='Category:N'
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(source).mark_point().encode(
    x='Date:T',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'Value:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(source).mark_rule(color='gray').encode(
    x='Date:T',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
chart= alt.layer(
    line, selectors, points, rules, text
)

st.altair_chart(chart, use_container_width=True)

# short messages: stock vs. market return
stock_return = ((stock_index_data[str(select_stock)][-1] - stock_index_data[str(select_stock)][0])/stock_index_data[str(select_stock)][0])*100
stock_return = round(stock_return,2)
st.write('#### First stock ('+select_stock+') return:', stock_return, '%')

stock_return2 = ((stock_index_data[str(select_stock2)][-1] - stock_index_data[str(select_stock2)][0])/stock_index_data[str(select_stock2)][0])*100
stock_return2 = round(stock_return2,2)
st.write('#### Second stock ('+select_stock2+') return:', stock_return2, '%')

index_return = ((stock_index_data['Crobex_value'][-1] - stock_index_data['Crobex_value'][0])/stock_index_data['Crobex_value'][0])*100
index_return = round(index_return,2)
st.write('#### Crobex return during analysed period:', index_return, '%')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

