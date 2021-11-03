# CryptoMonitor
Scrapes 4chan's business board for mentions of Cryptocurrencies, then writes data to an Excel file

CryptoFind.py and CoinDict.py are nescessary files, CryptoFind Calls Coin Dict to determine Crypto currency names. The Excel file it writes to is called tester.xlsx

ReadtoRFile is an optional bit of code that reads from the Excel file into R code to make it easy to examine the data with R.


# Graphing
Done using plotly. Json is converted to dataframes using pandas 

# Changelog
#### 1.01
* kucoin intergration to get coin names and market data.
* Revision of chan scraper to account for post id digit increase
* Progress bar for thread parsing 
* Changed to use chromium (default exe location C:/windows)
* .env file for kucoin api keys
#### 1.02
* Added mongodb db support 
* Record tickers into collection 
* Ticker blacklist for common word ticker names 
* Ability to extract image,message,mentions from thread
#### 1.03
* update ticker blacklist
* created scraper for chan archieves 
#### 1.04
* Added graphing using plotly and dash of coins mentions in /biz
* Sort graphed coins by marketcap
* Coin name/symbol translation between coingecko and kucoin
* Added multithreading for archieve data collection
#### 1.05
* Individual coin selector
* Show price when view individual coin
* Pickled coingecko coin data to reduce api requests
* Moving plotly server to main directory to be ran directly 

# Todo
* Switch from kucoin to fully coingecko for ticker finder 
* If ticker is found in OP text add ticker instance for each comment 
* When clicking on graph data show references
* Get mentions moving average
* Add daily volume with price
* Change price/volume data to only get days from earlist mention data


# How_to
1) Key kucoin api read only api keys and insert into .env (using .env_example as template)
2)
```python
python3.7 .\getThreads.py -s 21000 -e 21010 -p 10  
```

## Update requirements
```py
python3.7 -m pipreqs.pipreqs --force
```