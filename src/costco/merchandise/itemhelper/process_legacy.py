from create_views import *
from csvin import *
import settings
import os

# Import legacy tables from .csv files on the MicroSD card
os.chdir(settings.IMPORT_PATH)
for entry in os.listdir(settings.IMPORT_PATH):
    entry_name, entry_extension = os.path.splitext(entry)
    if entry_extension == '.csv':
        CSVTable(entry, settings.ENCODING).create(settings.DB_PATH, entry_name)

# Daily sales view
ViewBuilder().build(
    'daily_sales',
    'item',
    'select rowid _id, saitem item, sawhse whs, safyr fyear, safwk fweek, \
     samons m, satues t, saweds w, sathus th, safris f, sasats sa, sasuns su, \
     (samons + satues + saweds + sathus + safris + sasats + sasuns) \
     total_week from indlyip'  
)
     
# Adjusted daily average sales summary table 
TableBuilder().build(
    'avg_daily_sales', 
    'item',
    'select _id, item, whs, fyear, adjustedaverage(m) m, \
     adjustedaverage(t) t, \
     adjustedaverage(w) w, adjustedaverage(th) th, adjustedaverage(f) f, \
     adjustedaverage(sa) sa, adjustedaverage(su) su, \
     adjustedaverage(total_week) \
     week from daily_sales group by item, whs, fyear',
    [],
    [AdjustedAverage]
)
