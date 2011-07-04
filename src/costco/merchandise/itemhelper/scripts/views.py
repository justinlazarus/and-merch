import builders
import analysis

# Drop and create the available views table
builders.AvailableViews().drop()
builders.AvailableViews().create()

""" VIEW fiscal_years 

Gets the first day of every fiscal year from the information available in 
INFLSHP. This file contains all sales information for every day in the 
region, so it also contains the start date of every fiscal year.

"""
builders.View(
    'fiscal_years',
    'flash',
    ['inflshp',],
    'select distinct flfyr fiscal_year, fldate start_date from inflshp where \
    flper=1 and flweek=1 and flday=1'
).build()

""" VIEW daily_sales 

Packages the information in INDLYIP into a more usable format. Includes 
gregorian dates and the weekly total units sold.

"""
builders.View(
    'daily_sales',
    'item',
    ['indlyip',],
    'select rowid _id, saitem item, sawhse whs, safyr fyear, safwk fweek, \
     samons m, satues t, saweds w, sathus th, safris f, sasats sa, sasuns su, \
     (samons + satues + saweds + sathus + safris + sasats + sasuns) \
     total_week from indlyip'  
).build()
     
""" VIEW average_daily_sales

Building off the daily_sales view, this view runs an aggregate function over a 
grouping of the sales over the entire year. The results are a row for every 
item in the daily_sales view. Each column in this row is the adjusted average
sales for that day, or for the entire week in the case of the last column. 
For more information on how the adjusted average function works, see 
analysis.AdjustedAverage. 
 
"""
builders.View(
    'average_daily_sales', 
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

""" VIEW weekly_sales

This view makes the INIHSTP file more useable by running a massive union to 
join a selection of each week column in the original table. This union 
effectively normalizes the table, resulting in a row for each fiscal week for
each item, instead of a row for each fiscal year for each item, and a column 
for each week. This allows for the use of aggregate functions over the weekly
sales data, such as adjusted average, that would not be possible on the 
legacy file. Piece of shit legacy files! 

"""
builders.View(
    'weekly_sales',
    'item',
    ['inihstp',],
    ' '.join(
        ['select ihwhse, ihfyr, %s ihfwk, ihdept, ihitem, ihs$%02d \
        from inihstp union all' % (week, week) for week in range(1,53)]
    ) + ' select ihwhse, ihfyr, 53 ihfwk, ihdept, ihitem, ihs$53 \
        from inihstp'
).build()
