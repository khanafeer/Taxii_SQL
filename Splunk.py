import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



class Splunk():
    
    def __init__(self, url, app, user, password,kv_name):
        self.url = url
        self.app = app
        self.user = user
        self.password = password
        self.kv_name = kv_name
        self.template = """type,value
string,string"""

    def get_date_from_dic(self, value,key):
        try:
            for k, v in value.items():
                try:
                    return v[key]
                except:
                    pass
        except:pass
        return "N\A"

    def createKVStore(self):
        try:
            splunk_url = ''.join([self.url, '/servicesNS/nobody/', self.app,
                                  '/storage/collections/config', self.kv_name])
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(splunk_url, auth=(self.user, self.password), verify=False, headers=headers,
                              data=self.template)
            print(r.text)
        except Exception as e:
            print(e)

    def configureKVStore(self):
        try:
            splunk_url = ''.join([self.url, '/servicesNS/nobody/', self.app,
                                  '/storage/collections/config/', self.kv_name])
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(splunk_url, auth=(self.user, self.password), verify=False, headers=headers,
                              data=self.template)
            print(r.text)
        except Exception as e:
            print(e)

    def insertKVItem(self, item_j):
        try:
            splunk_url = ''.join([self.url, '/servicesNS/nobody/', self.app,
                                  '/storage/collections/data/', self.kv_name])
            headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(splunk_url, auth=(self.user, self.password), verify=False,headers=headers,
                              json=item_j)
            print("IOC Added Successfully -- KV Store ID :", r.json()['_key'])
        except Exception as e:
            print("[Error] Splunk Inserting Exception --", e)
