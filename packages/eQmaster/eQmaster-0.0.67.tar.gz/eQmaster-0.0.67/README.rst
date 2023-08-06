**eQmaster** is a python package that allows user to retrieve stock data fast and compact. 

**Main Features**
- use **get(stock_list, from_date, to_date)** to get stock data between **from_date** and **to_date**. Date is formatted as *YYYY-MM-DD*. The latest **to_date** value is one day prior to the current date.

- use **get_current_quote(stock_symbol)** to get most updated stock quote. It is currently supported for single stock prices quote. 

- use **is_market_open(market_name)** to determine if given market is open for trades. It is currently supported for Taiwanese stock market only.

- use **setup(settings=None)** to determine if given market is open for trades. It is currently supported for Taiwanese stock market only.

