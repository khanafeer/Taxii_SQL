from taxii2client.v21 import Server, Collection, as_pages
from Splunk import Splunk
from Qradar import Qradar
import datetime
from threading import Thread
import json
import time

class TaxiiCollection(Thread):

    def __init__(self, taxii_url, collection, taxii_user, taxii_pass, date_time):
        Thread.__init__(self)
        self.taxii_url = taxii_url
        self.collection = collection
        self.taxii_user = taxii_user
        self.taxii_pass = taxii_pass
        self.date_time = date_time

    def get_manifest(self):
        collection = Collection(self.taxii_url + self.collection, user=self.taxii_user, password=self.taxii_pass)
        feeds = collection.get_manifest()
        return feeds

    def get_collection_data(self, date):
        try:
            collection = Collection(self.taxii_url + self.collection,
                                    user=self.taxii_user, password=self.taxii_pass)
            feeds = as_pages(collection.get_objects,  per_request=50, added_after=date)
            return feeds
        except Exception as ex:
            print("[Error] Taxii Get Collections Exception --", ex)

    def run(self):
        # Reading Customers Config File
        try:
            self.customers = json.loads(open("customers.conf").read())
        except Exception as ex:
            print("[ERROR] Customers Config File Error (JSON Only) -- ", ex)
            exit()
        # Fetching Feeds as pages for last 13 hours
        date_time = self.date_time - datetime.timedelta(hours=13)
        feeds = self.get_collection_data(str(date_time))
        for feed_obj in feeds:
            try:
                for feed in feed_obj['objects']:
                    # Looping over customers to import
                    for customerk, customerv in self.customers.items():
                        print("[INFO] Selecting Customer --", customerk)
                        if customerv['SIEM'] == 'qradar':
                            qrd = Qradar(customerv['url'], customerv['username'], customerv['password'])
                            ISTIP_Feeds = customerv['reference'] + "_" + qrd.get_date_from_dic(feed['extensions'],
                                                                                 "main_observable_type")
                            qrd.set_reference_values(ISTIP_Feeds, {"value": str(feed['name'])})
                        elif customerv['SIEM'] == 'splunk':
                            # Splunk Importing
                            spl = Splunk(customerv['url'], customerv['app'], customerv['username'],
                                         customerv['password'],
                                         customerv['reference'])
                            spl.insertKVItem(
                                {"type": spl.get_date_from_dic(feed['extensions'], "main_observable_type"),
                                 "_key": feed['name'],
                                 "created": spl.get_date_from_dic(feed['extensions'], "created_at"),
                                 'imported': str(datetime.datetime.now())})
                        elif customerv['SIEM'] == 'logrhythm':
                            # LR importing
                            print("[ERROR] LR Importing Not Supported Yet")
                        else:
                            print("[ERROR] Not Supported SIEM -- Only Splunk, Qradar, and LR.")
            except Exception as ex:
                print("[Error] IOC inserting Main Exception --", ex)