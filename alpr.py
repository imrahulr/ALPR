from openalpr import Alpr
import sys
import sqldb
import numpy as np

alpr = Alpr("eu", "openalpr/config/openalpr.conf", "openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error.... Failed to Load ALPR!")

mysql = sqldb.sqldb("alpr", "user")
mysql.get_table_count()

alpr.set_top_n(5)
results = alpr.recognize_file("in.jpeg")

i = 0
for plate in results['results']:
    i += 1
    print("Plate #%d" % i)
    print("   %12s %12s" % ("Plate", "Confidence"))
    for candidate in plate['candidates']:
        prefix = "-"
        if candidate['matches_template']:
            prefix = "*"
        print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
        
plateno = results['results'][0]['candidates'][0]['plate']
start_x = min(results['results'][0]['coordinates'][0]['x'], results['results'][0]['coordinates'][3]['x'])
start_y = min(results['results'][0]['coordinates'][0]['y'], results['results'][0]['coordinates'][1]['y'])
end_x = max(results['results'][0]['coordinates'][1]['x'], results['results'][0]['coordinates'][2]['x']) 
end_y = max(results['results'][0]['coordinates'][2]['y'], results['results'][0]['coordinates'][3]['y'])

mysql.search_db(plateno)

mysql.debit(plateno, 100)
mysql.credit(plateno, 100)
alpr.unload()