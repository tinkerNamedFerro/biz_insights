# CryptoMonitor
Scrapes 4chan's business board for mentions of Cryptocurrencies, then writes data to an Excel file

CryptoFind.py and CoinDict.py are nescessary files, CryptoFind Calls Coin Dict to determine Crypto currency names. The Excel file it writes to is called tester.xlsx

ReadtoRFile is an optional bit of code that reads from the Excel file into R code to make it easy to examine the data with R.

# Update
#### 1.01
* kucoin intergration to get coin names and market data.
* Revision of chan scraper to account for post id digit increase
* Progress bar for thread parsing 
* Changed to use chromium (default exe location C:/windows)
* .env file for kucoin api keys


# Todo
* Save data into json format (mongodb)
* Record post/comment time stamps


# How_to
1) Key kucoin api read only api keys and insert into .env (using .env_example as template)
2)
```python
python3.7 .\CryptoFinder.py
```