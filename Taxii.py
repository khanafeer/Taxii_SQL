from taxii2client.v21 import Server, Collection, as_pages
from Splunk import Splunk
from Qradar import Qradar
import datetime
from threading import Thread
import json
import time

class TaxiiCollection(Thread):

    def __init__(self, taxii_url, collection, taxii_user, taxii_pass,customer_name, customer):
        Thread.__init__(self)
        self.taxii_url = taxii_url
        self.collection = collection
        self.taxii_user = taxii_user
        self.taxii_pass = taxii_pass
        self.customer_name = customer_name
        self.customer = customer

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

    def update_config_customer_first(self):
        config = json.loads(open("config.conf").read())
        config["customers"][self.customer_name]['FIRST'] = 0
        f = open("config.conf", "w+")
        f.write(str(config))
        f.close()
    def run(self):
        # Fetching Feeds as pages for last 13 hours, or all feeds if it's first time
        print("FIRST" , self.customer.get('FIRST'), type(self.customer.get('FIRST')))
        if self.customer.get('FIRST'):
            date_time = datetime.date(year=2018, month=1, day=1)
            self.update_config_customer_first()
        else:
            date_time = datetime.datetime.now()
        date_time = date_time - datetime.timedelta(hours=13)
        feeds = self.get_collection_data(str(date_time))
        for feed_obj in feeds:
            try:
                for feed in feed_obj['objects']:
                    if self.customer['SIEM'] == 'qradar':
                        qrd = Qradar(self.customer['url'], self.customer['username'], self.customer['password'])
                        ISTIP_Feeds = self.customer['reference'] + "_" + qrd.get_date_from_dic(feed['extensions'],
                                                                                           "main_observable_type")
                        qrd.set_reference_values(ISTIP_Feeds, {"value": str(feed['name'])})
                    elif self.customer['SIEM'] == 'splunk':
                        # Splunk Importing
                        spl = Splunk(self.customer['url'], self.customer['app'], self.customer['username'],
                                     self.customer['password'],
                                     self.customer['reference'])
                        spl.insertKVItem(
                            {"type": spl.get_date_from_dic(feed['extensions'], "main_observable_type"),
                             "_key": feed['name'],
                             "created": spl.get_date_from_dic(feed['extensions'], "created_at"),
                             'imported': str(datetime.datetime.now())})
                    elif self.customer['SIEM'] == 'logrhythm':
                        # LR importing
                        print("[ERROR] LR Importing Not Supported Yet")
                    else:
                        print("[ERROR] Not Supported SIEM -- Only Splunk, Qradar, and LR.")
            except Exception as ex:
                print("[Error] IOC inserting Main Exception --", ex)