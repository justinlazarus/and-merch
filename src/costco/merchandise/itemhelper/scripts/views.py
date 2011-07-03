import builders
import analysis

# Fiscal Years view
builders.View(
    'fiscal_years',
    'flash',
    ['inflshp',],
    'select distinct flfyr fiscal_year, fldate start_date from inflshp where \
    flper=1 and flweek=1 and flday=1'
).build()

# Daily sales view
builders.View(
    'daily_sales',
    'item',
    ['indlyip',],
    'select rowid _id, saitem item, sawhse whs, safyr fyear, safwk fweek, \
     samons m, satues t, saweds w, sathus th, safris f, sasats sa, sasuns su, \
     (samons + satues + saweds + sathus + safris + sasats + sasuns) \
     total_week from indlyip'  
).build()
     
# Adjusted daily average sales summary table 
builders.View(
    'avg_daily_sales', 
    'item',
    ['daily_sales',],
    'select _id, item, whs, fyear, adjustedaverage(m) m, \
     adjustedaverage(t) t, \
     adjustedaverage(w) w, adjustedaverage(th) th, adjustedaverage(f) f, \
     adjustedaverage(sa) sa, adjustedaverage(su) su, \
     adjustedaverage(total_week) \
     week from daily_sales group by item, whs, fyear',
    [],
    [analysis.AdjustedAverage]
).build()
