# RR4005i to InfluxDB Collector
Pull power statistics fro a [West Mountain Radio RR4005i](https://www.westmountainradio.com/product_info.php?products_id=rr_4005i) and push it into InfluxDB.

## Setup
```
python3 -m venv venv
pip install -r requirements.txt
```

Edit rr4005_stats.sh and update env vars with appropriate settings.

Setup crontab to run rr4005_stats.sh every minute.

## InfluxDB Data Point

Example XML data from a RR4005i:
```
<rr4005i>
   <SUPPLY>13.72</SUPPLY>
   <RAILLOAD0>1.33</RAILLOAD0>
   <RAILLOAD1>1.52</RAILLOAD1>
   <RAILLOAD2>1.65</RAILLOAD2>
   <RAILLOAD3>1.11</RAILLOAD3>
   <RAILLOAD4>0.54</RAILLOAD4>
   <RAILENA0>1</RAILENA0>
   <RAILENA1>1</RAILENA1>
   <RAILENA2>1</RAILENA2>
   <RAILENA3>1</RAILENA3>
   <RAILENA4>1</RAILENA4>
</rr4005i>
```

Data is added in the following format:
```
{
    'measurement': 'rr4005_power', 
    'tags': {'name': 'RR4005'}, 
    'fields': {
        'supply_voltage': 13.72, 
        'rail_load_0': 1.33,
        'rail_load_1': 1.52,
        'rail_load_2': 1.65,
        'rail_load_3': 1.11,
        'rail_load_4': 0.54,
        }
}
```