import time
import datetime
import sys

from Taxii import TaxiiCollection

FIRST = True
if FIRST:
    date_time = datetime.date(year=2018, month=1, day=1)
else:
    date_time = datetime.datetime.now()

while True:
    try:
        # enable file logging
        # log_file = open("error.log", "a+")
        # sys.stdout = log_file
        print("[INFO] Running The Thread Class")
        collection = TaxiiCollection(taxii_url="http://127.0.0.1:8443/taxii2/root/collections/",
                                   collection="c69c0965-831a-466a-a7c2-4cf82f02393c",
                                   taxii_user="user@domain.com",
                                   taxii_pass="TI@123",
                                   date_time= date_time)
        collection.run()
    except Exception as ex:
        print("[ERROR] Threading Error --", ex)
    finally:
        # sleeping for 6Hours = 21600 sec
        print("[INFO] Sleeping for a while -- zzzzzzzzz")
        #log_file.close()
        time.sleep(21600)
