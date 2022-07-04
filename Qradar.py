import json
import requests


class Qradar():
    def __init__(self, url, user,password):
        self.url = url
        self.user = user
        self.password = password
        self.headers = {'Accept': 'application/json', 'Content-type': 'application/json'}

    def create_reference_set(self, ISTIP_Feeds):
        try:
            ref_sets_url = self.url + f'/api/reference_data/sets/{ISTIP_Feeds}'
            creation_url = self.url + f'/api/reference_data/sets?element_type=ALN&name={ISTIP_Feeds}'
            print("[INFO] Checking for reference set")
            req = requests.get(ref_sets_url, headers=self.headers, verify=False, auth=(self.user, self.password))
            if req.status_code != 404:
                    print(f"[INFO] Reference set Already Exist -- {ISTIP_Feeds}")
                    return ISTIP_Feeds
            else:
                r = requests.post(creation_url, self.headers, verify=False, auth=(self.user, self.password))
                if r.status_code in [200, 201]:
                    print(f"[INFO] Reference set Created For First Time -- {ISTIP_Feeds}")
                    return ISTIP_Feeds
                else:
                    print("[ERROR] Reference set Creation Error -- ", r.text)
            return "N\\A"
        except Exception as ex:
            print("[ERROR] Reference set Check Exception -- ", ex)

    def set_reference_values(self, reference, value):
        self.create_reference_set(reference)
        url = self.url + "/api/reference_data/sets/" + reference

        try:
            response = requests.post(url, value, self.headers, auth=(self.user, self.password), verify=False)
            body = response.json()
            print("[INFO] IOC Imported -- ", value)
        except Exception as Ex:
            print("[Error] Importing IOCs Error -- ", Ex)
            print(body)


    def get_date_from_dic(self, value,key):
        try:
            for k, v in value.items():
                try:
                    return v[key]
                except:
                    pass
        except:pass
        return "N\A"