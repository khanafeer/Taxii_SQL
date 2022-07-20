import time
import datetime
import sys
import json

from Taxii import TaxiiCollection

while True:
    try:
        # enable file logging
        # log_file = open("error.log", "a+")
        # sys.stdout = log_file
        try:
            config = json.loads(open("config.conf").read())
            taxii = config.get("taxii")
            customers = config.get("customers")
            print("[INFO] Running The Thread Class")
            for customerk, customerv in customers.items():
                print("[INFO] Selecting Customer --", customerk)
                collection = TaxiiCollection(taxii_url=taxii.get("taxii_url"),
                                         collection=taxii.get("collection"),
                                         taxii_user=taxii.get("taxii_user"),
                                         taxii_pass=taxii.get("taxii_pass"),
                                        customer_name=customerk,
                                         customer= customerv)
                collection.run()
        except Exception as ex:
            print("[ERROR] Customers Config File Error (JSON Only) -- ", ex)
    except Exception as ex:
        print("[ERROR] Threading Error --", ex)
    finally:
        # sleeping for 6Hours = 21600 sec
        print("[INFO] Sleeping for a while -- zzzzzzzzz")
        #log_file.close()
        time.sleep(21600)
