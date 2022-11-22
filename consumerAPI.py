import requests
import json
api_url = "https://Avenue.reliancegeneral.co.in/vmsintegration/Attendance"
requestbody = {"Employee_Code": "70299794","Login_Date": "04/03/2021","In_Time": "09:30","Log_Flag": "Entry"}
headers =  {"Ocp-Apim-Subscription-Key" : "e8f1d1a426954e8da25ab71f6f8813c9"}
response = requests.post(api_url, data=json.dumps(requestbody), headers=headers)
response.json()
response.status_code