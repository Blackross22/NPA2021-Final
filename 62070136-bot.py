import time
from webbrowser import get
import requests
import json
from ncclient import manager

std_id = "62070136"
access_token = 'YTc0NzljYmMtZWYyNy00ZDQzLTkxZDMtOGQxNTIzMTU3YzhhZDMwZjBiOTktNThj_P0A1_79e3e991-eb8c-4b22-ad21-c09700548c09'
url = 'https://webexapis.com/v1/messages'
room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjUwODkzMjAtY2QxOS0xMWVjLWE1NGUtNGQ2MmNhMWM4YmVl'
headers = {
'Authorization': 'Bearer {}'.format(access_token),
'Content-Type': 'application/json'
}
def get_massage():
    res = requests.get(url, headers=headers, params={'roomId': room_id})
    text = res.json()["items"][0]["text"]
    return (text)

def post_massage(text ,status):
    if  text == std_id and status == True:
        params = {'roomId': room_id, 'markdown': "Loopback62070136 - Operational status is up"}
        res = requests.post(url, headers=headers, json=params)
        print(res.json())
    elif text == std_id and status == False:
        params = {'roomId': room_id, 'markdown': "Loopback62070136 - Operational status is down"}
        res = requests.post(url, headers=headers, json=params)
        print(res.json())
        
def get_info():
    m = manager.connect(
        host="10.0.15.106",
        port=830,
        username="cisco",
        password="cisco",
        hostkey_verify=False
        )
    netconf_filter = """
    <filter>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback>
                </Loopback>
            </interface>
        </native>
    </filter>
    """

    netconf_reply = m.get(filter=netconf_filter)
    if "<shutdown/>" in str(netconf_reply):
        return False
    else:
        return True

print(get_info())
def main():
    while(1):
        text = get_massage()
        print(text)
        info = get_info()
        post_massage(text, info)
        time.sleep(1)
main()