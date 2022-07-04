# Taxii_SQL

Taxii Splunk Qradar logrhythm Connector
This script helps you to Pull feeds from Taxii server and Push to SIEM solutions,
as the current implementation SIEM TI applications have alot of issues with the Taxii 2.

Used and tested with OpenCTI, Splunk, and Qradar.

### Usage
1. Install the requirements
```python
pip3 install -r requirements.txt
```
2. If it was not the first time to run the script, change value of FIRST variable, otherwise keep it.
```python
FIRST = False
```
3. Add your customers data in the customers.conf file as JSON format
```JSON
{
"customer1": {"SIEM":"splunk","url":"https://10.10.10.20:8089", "username":"admin", "password": "12345", "app":"launcher","reference":"TIP_Feeds"},
"customer2": {"SIEM":"qradar","url":"https://10.10.10.30", "username":"admin", "password": "12345", "app":"launcher","reference":"TIP_Feeds"}
}
```

4. run the script and it will push and pull every 12 hours
```python
python3 main.py
```

### Next Steps
- [ ] Logrhythm Support
- [ ] Performance Enhancement
