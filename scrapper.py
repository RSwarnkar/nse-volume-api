# Reference: https://stackabuse.com/deploying-a-flask-application-to-heroku/
# Github: https://github.com/RSwarnkar/nse-volume-api

# TO DO: https://flask.palletsprojects.com/en/2.0.x/patterns/packages/

# http://<Server_URL>/getrange?symbol=DRREDDY&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=23-05-2021&toDate=25-05-2021&dataType=PRICEVOLUMEDELIVERABLE

# Global Error messages: 

SUCCESS = {"Success": "True"}
APPERR_INVALID_PARAM = {"App Error": "True", "App Error Description": "Invalid Parameter"}

# GLOBAL IMPORTS: 

import requests
import pandas

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



# scrapper.py
from flask import Flask, request, jsonify
scrapper = Flask(__name__)

@scrapper.route('/getrange/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)
    
    _symbol = request.args.get("symbol", None)
    _segmentLink = request.args.get("segmentLink", 3)
    _symbolCount = request.args.get("symbolCount", 1)
    _series = request.args.get("series", "EQ")
    _dateRange = request.args.get("dateRange", "+") # Validation Needed
    _fromDate = request.args.get("fromDate", None)  # Validation Needed
    _toDate = request.args.get("toDate", None) # Validation Needed
    _dataType = request.args.get("dataType", "PRICEVOLUMEDELIVERABLE")
 
    # For debugging
    print(f"===Start of Params===")
    print(f"got symbol:{_symbol}")
    print(f"got segmentLink:{_segmentLink}")
    print(f"got symbolCount:{_symbolCount}")
    print(f"got series:{_series}")
    print(f"got dateRange:{_dateRange}")
    print(f"got fromDate:{_fromDate}")
    print(f"got toDate:{_toDate}")
    print(f"got dataType:{_dataType}")
    print(f"===End of Params===")

 
    # Default 
    response = {}
    response["__metaversion__"] = "nse-volume-api v1.0"


# VALIDATIONS SHOULD GO HERE --------------------
#    # Check if user sent a name at all
#    if not name:
#        response["ERROR"] = ""
#    # Check if the user entered a number not a name
#    elif str(name).isdigit():
#        response["ERROR"] = "name can't be numeric."
#    # Now the user entered a valid name
#    else:
#        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"
        
    # Main Logic: 
    sess = requests.Session()
    rs = sess.get(NSE_URL1, headers=HEADER_REQ1)
    
    arr_cookies = [{'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path, 'expires': c.expires} for c in sess.cookies]
    parsed_cookies = arr_cookies[0].get('name') + "=" + arr_cookies[0].get('value')
    
    custom_query_params = {
    'symbol': _symbol,
    'segmentLink': _segmentLink,
    'symbolCount': _symbolCount,
    'series': _series,
    'dateRange': _dateRange,
    'fromDate': _fromDate,
    'toDate': _toDate,
    'dataType': _dataType}
    
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
    
    rs = requests.get("https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp", params=custom_query_params,headers=custom_headers)
    parsed_tables = pandas.read_html(rs.text)
    df = pandas.DataFrame(parsed_tables[0])

    final_response = str(df.to_json())
     
    # Return the response in json format
    return final_response



# A welcome message to test our server
@scrapper.route('/')
def index():
    return  "{\"__metaversion__\":\"nse-volume-api v1.0\"}"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    #scrapper.run(threaded=True, port=5000)
    scrapper.run()