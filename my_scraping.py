import pandas as pd
import time

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
    df_stocks_ISIN['merged'].to_csv('stocks_symbols_and_ISIN.csv', index=False)
    
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    