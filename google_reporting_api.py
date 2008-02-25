#!/usr/bin/python

# Sample code for google reporting API
# More info on http://code.google.com/apis/apps/reporting/google_apps_reporting_api.html


import httplib, urllib
email = ""
passwd = ""
domain = "jnanaprabodhini.org"
date = "2007-12-01"
report_type = "daily"
report_name = "disk_space"

params = urllib.urlencode({'accountType': "HOSTED", 'Email': email, 'Passwd': passwd})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPSConnection("www.google.com")
conn.request("POST", "/accounts/ClientLogin", params, headers)
response = conn.getresponse()
data = response.read()
conn.close()
data = data.split('\n')
authtoken = data[0].split('=')[1]

envelope = """<?xml version="1.0" encoding="UTF-8"?>
<rest xmlns="google:accounts:rest:protocol"
    xmlns:xsi=" http://www.w3.org/2001/XMLSchema-instance ">
    <type>Report</type>"""
envelope += "<token>"+authtoken+"</token>"
envelope += "<domain>"+domain+"</domain>"
envelope += "<date>"+date+"</date>"
envelope += "<reportType>"+report_type+"</reportType>"
envelope += "<reportName>"+report_name+"</reportName>"
envelope += "</rest>"
envlen = len(envelope) 

http_conn = httplib.HTTPS('www.google.com')
http_conn.putrequest('POST', '/hosted/services/v1.0/reports/ReportingData')  
http_conn.putheader('Content-Type', 'text/xml; charset="utf-8"') 
http_conn.putheader('Content-Length', str(envlen)) 
http_conn.endheaders() 
http_conn.send(envelope)
(status_code, message, reply_headers) = http_conn.getreply() 
response = http_conn.getfile().read() 
print response
