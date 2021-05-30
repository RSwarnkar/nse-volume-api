# NSE Volume Data API 
This is a simple Python Flask based API which fetches the data from [National Stock Exchange (NSE), India](https://www1.nseindia.com/products/content/equities/equities/eq_security.htm)'s website and responds Security-wise Price, Volume and Deliverable Position Data. 


## Fields in JSON response:

List of fields in JSOn response: 
```
Symbol
Series
Date
Prev Close
Open Price
High Price
Low Price
Last Price
Close Price
VWAP
Total Traded Quantity
Turnover
No. of Trades
Deliverable Qty
% Dly Qt to Traded Qty```

Here is sample data: 

```
{"Symbol":{"0":"DRREDDY","1":"DRREDDY"},"Series":{"0":"EQ","1":"EQ"},"Date":{"0":"24-May-2021","1":"25-May-2021"},"Prev Close":{"0":5216.45,"1":5272.15},"Open Price":{"0":5236.0,"1":5289.4},"High Price":{"0":5299.0,"1":5320.0},"Low Price":{"0":5226.7,"1":5255.0},"Last Price":{"0":5276.0,"1":5317.0},"Close Price":{"0":5272.15,"1":5311.2},"VWAP":{"0":5263.55,"1":5288.97},"Total Traded Quantity":{"0":706498,"1":695615},"Turnover":{"0":3718685094.0500001907,"1":3679085487.3499999046},"No. of Trades":{"0":43435,"1":45531},"DeliverableQty":{"0":171828,"1":209379},"% Dly Qt toTraded Qty":{"0":24.32,"1":30.1}}
```


### Disclaimer: 
Standard Disclaimers applied. Use at your own risk. 
