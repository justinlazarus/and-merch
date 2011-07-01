from create_views import *
from csvin import *
import os

IMPORT_PATH = '/Removable/MicroSD/merch/'

# Import legacy tables from .csv files on the MicroSD card
os.chdir(IMPORT_PATH)
for entry in os.listdir(IMPORT_PATH):
    entry_name, entry_extension = os.path.splitext(entry)
    if entry_extension == '.csv':
        CSVTable(entry, 'big5').create('sales.db', entry_name)

# Create all views and summary tables
tb = TableBuilder()
vb = ViewBuilder()

# Daily sales view
vb.build(
    'daily_sales',
    'select rowid _id, saitem item, sawhse whs, safyr fyear, safwk fweek, \
     samons m, satues t, saweds w, sathus th, safris f, sasats sa, sasuns su, \
     (samons + satues + saweds + sathus + safris + sasats + sasuns) \
     total_week from indlyip'  
)
     
# Adjusted daily average sales summary table 
tb.build(
    'avg_daily_sales', 
    'select _id, item, whs, fyear, adjustedaverage(m) m, \
     adjustedaverage(t) t, \
     adjustedaverage(w) w, adjustedaverage(th) th, adjustedaverage(f) f, \
     adjustedaverage(sa) sa, adjustedaverage(su) su, \
     adjustedaverage(total_week) \
     week from daily_sales group by item, whs, fyear',
    [],
    [AdjustedAverage]
)
