# Reference: https://stackabuse.com/deploying-a-flask-application-to-heroku/
# Github: https://github.com/RSwarnkar/nse-volume-api

# TO DO: https://flask.palletsprojects.com/en/2.0.x/patterns/packages/

# http://<Server_URL>/getrange?symbol=DRREDDY&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=23-05-2021&toDate=25-05-2021&dataType=PRICEVOLUMEDELIVERABLE

#symbol=DMART&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=26-05-2021&toDate=30-05-2021&dataType=PRICEVOLUMEDELIVERABLE

# GLOBAL IMPORTS: 

import requests
import pandas
import os
import datetime
import numpy as np 

# GLOBAL VARS: 

NSE_URL1 = 'https://www1.nseindia.com/products/content/equities/equities/eq_security.htm'

HEADER_REQ1 = {
"Host" : "www1.nseindia.com",
"Connection" : "keep-alive",
"sec-ch-ua":   "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
"sec-ch-ua-mobile": "?0",
"Upgrade-Insecure-Requests" : "1",
"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site" : "none",
"Sec-Fetch-Mode" : "navigate",
"Sec-Fetch-User" : "?1",
"Sec-Fetch-Dest" : "document",
"Accept-Encoding" : "gzip, deflate, br",
"Accept-Language" : "en-US,en;q=0.9"
}

DEBUG = True 


def iqr_Anomaly_Upper(datalist,sample):
    if (datalist is None):
        return -1
    # convert to Numpy array. Easy to apply qunatile funtion 
    datalist = np.array(datalist)
    
    Q3, Q1 = np.percentile(datalist, [75 ,25])
    IQR = Q3 - Q1
    
    IQR_ANOMALY_UPPER_THRESHOLD = Q3 + 1.5 * IQR

    if(sample>=IQR_ANOMALY_UPPER_THRESHOLD):
        return 1  # Sample shows high volume activity 
    else:
        return 0  # Sample is normal volume activity 




def fetchDataFromNSE(_symbol_list,_lastndays=21): 
    
    
    date_past = str(datetime.date.today() - pandas.offsets.DateOffset(days=_lastndays)).split(" ")[0]
    date_today  = str(datetime.date.today() - pandas.offsets.DateOffset(days=0)).split(" ")[0]
    
    date_past_obj = datetime.datetime.strptime(date_past, '%Y-%m-%d')
    date_today_obj = datetime.datetime.strptime(date_today, '%Y-%m-%d')
    
    
    date_past = date_past_obj.strftime('%d-%m-%Y')
    date_today = date_today_obj.strftime('%d-%m-%Y')

    print("date from ", date_past, type(date_past))
    print("date today ",date_today, type(date_today))
    
    
    #_symbol = "DMART"
    _segmentLink = "3"
    _symbolCount = "1"
    _series = "EQ"
    _dateRange = "+"
    _fromDate = date_past
    _toDate = date_today
    _dataType = "PRICEVOLUMEDELIVERABLE"
    
 
    
    # For debugging
    #print(f"===Start of Params===")
    ##print(f"got symbol:{_symbol}")
    #print(f"got segmentLink:{_segmentLink}")
    #print(f"got symbolCount:{_symbolCount}")
    #print(f"got series:{_series}")
    #print(f"got dateRange:{_dateRange}")
    #print(f"got fromDate:{_fromDate}")
    #print(f"got toDate:{_toDate}")
    #print(f"got dataType:{_dataType}")
    #print(f"===End of Params===")
    
       
 
    sess = requests.Session()
    rs = sess.get(NSE_URL1, headers=HEADER_REQ1)
    
    arr_cookies = [{'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path, 'expires': c.expires} for c in sess.cookies]
    parsed_cookies = arr_cookies[0].get('name') + "=" + arr_cookies[0].get('value')
    
    custom_headers = {
            "Host" : "www1.nseindia.com",
            "Connection" : "keep-alive",
            "sec-ch-ua":   "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "Upgrade-Insecure-Requests" : "1",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Accept" : "*/*",
            "X-Requested-With" : "XMLHttpRequest",
            "Sec-Fetch-Site" : "same-origin",
            "Sec-Fetch-Mode" : "cors",
            "Sec-Fetch-Dest" : "empty" ,
            "Referer" : "https://www1.nseindia.com/products/content/equities/equities/eq_security.htm",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "en-US,en;q=0.9",
            "Cookie" : parsed_cookies}
    
    final_verdict =  ""
    
    for _symbol in _symbol_list:
    
        print("Checking: Stock: "+_symbol)
 
        rs = requests.get("https://www1.nseindia.com//marketinfo/sym_map/symbolCount.jsp?symbol="+_symbol,headers=custom_headers)
        _symbolCount = str(rs.text).strip()
        
        #print("After calling symbolCount.jsp: symbolCount="+_symbolCount)
        
        custom_query_params = {
           'symbol': _symbol,
           'segmentLink': _segmentLink,
           'symbolCount': _symbolCount,
           'series': _series,
           'dateRange': _dateRange,
           'fromDate': _fromDate,
           'toDate': _toDate,
           'dataType': _dataType}  
 
        rs = requests.get("https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp", params=custom_query_params,headers=custom_headers)
        parsed_tables = pandas.read_html(rs.text)
        df = pandas.DataFrame(parsed_tables[0])
        time_stamp_file = _symbol +"_"+str(datetime.datetime.now()).replace(" ","-").replace(":","-").replace(".","-") + ".csv"
        
        df.to_csv("temp/"+time_stamp_file)
        
        try: 
            df2 = df[['Date', 'Total Traded Quantity', 'DeliverableQty']].copy()
        
            Latest_Date = df2["Date"].to_numpy()[-1]
        
            Trade_Volume = df2["Total Traded Quantity"].to_numpy()
            Trade_Volume_Latest_Sample = df2["Total Traded Quantity"].to_numpy()[-1]
            
            Trade_Delivery = df2["DeliverableQty"].to_numpy()
            Trade_Delivery_Latest_Sample = df2["DeliverableQty"].to_numpy()[-1]
            
            if(iqr_Anomaly_Upper(Trade_Volume,Trade_Volume_Latest_Sample)==-1):
                trade_volume_result = "Trade Volume [For Date: "+Latest_Date+", Stock: "+_symbol + " = Invalid data. Please investigate cause.]"
              
            elif(iqr_Anomaly_Upper(Trade_Volume,Trade_Volume_Latest_Sample)==1):
                trade_volume_result = "Trade Volume [For Date: "+Latest_Date+", Stock: "+_symbol + " = indicates ABNOMALLY HIGH TRADING activity.]"
            
            elif(iqr_Anomaly_Upper(Trade_Volume,Trade_Volume_Latest_Sample)==0):
                trade_volume_result = "Trade Volume [For Date: "+Latest_Date+", Stock: "+_symbol + " = indicates normal trading activity.]"   
            
            
            if(iqr_Anomaly_Upper(Trade_Delivery,Trade_Delivery_Latest_Sample)==-1):
                delivery_result = "Trade Delivery [For Date: "+Latest_Date+", Stock: "+_symbol + " = Invalid data. Please investigate cause.]"
              
            elif(iqr_Anomaly_Upper(Trade_Delivery,Trade_Delivery_Latest_Sample)==1):
                delivery_result = "Trade Delivery [For Date: "+Latest_Date+", Stock: "+_symbol + " = indicates ABNOMALLY HIGH DELIVERY activity.]"
            
            elif(iqr_Anomaly_Upper(Trade_Delivery,Trade_Delivery_Latest_Sample)==0):
                delivery_result = "Trade Delivery [For Date: "+Latest_Date+", Stock: "+_symbol + " = indicates normal delivery activity.]"   
            
            final_verdict = final_verdict + "\n" + trade_volume_result + " " + delivery_result 
        except KeyError:
            final_verdict = final_verdict + "\n" + "Error fetching data for Stock: "+_symbol
 
    return final_verdict



def mainFunction():

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    stock_list = []
    with open(os.path.join(fileDir, 'stock-list/stocklist.txt')) as f:
        stock_list = f.read().splitlines()
        
    final_report = fetchDataFromNSE(stock_list, 28)
    
    report_filename = "reports/"+str(datetime.datetime.now()).replace(" ","-").replace(":","-").replace(".","-") + ".txt"
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
     
    with open(os.path.join(fileDir, report_filename), "w+") as f:
         f.write(final_report)
    
    print(final_report)
    
# Call main 
mainFunction()