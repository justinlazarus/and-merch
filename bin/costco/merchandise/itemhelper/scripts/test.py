import builders
from analsysis import get_gregorian_date

builders.View(
    'new_daily',
    'item',
    ['indlyip',],
    'select indlyip.rowid _id, saitem item, sawhse whse, safyr fyear, 
     safwk fweek, 1 day_of_week, samons sales, 
     get_geregorian_date(start_date, safwk, 1) date \
     from indlyip inner join fiscal_years on safyr = fiscal_year \

     union all \

     select rowid _id, saitem item, sawhse whse, safyr fyear, safwk fweek, \
     2 fday, satues sales from indlyip \
     union all \
     select rowid _id, saitem item, sawhse whse, safyr fyear, safwk fweek, \
     3 fday, saweds sales from indlyip \
     union all \
     select rowid _id, saitem item, sawhse whse, safyr fyear, safwk fweek, \
     4 fday, sathus sales from indlyip \
     union all \
     select rowid _id, saitem item, sawhse whse, safyr fyear, safwk fweek, \
     5 fday, safris sales from indlyip \
     union all \
     select rowid _id, saitem item, sawhse whse, safyr fyear, safwk fweek, \
     6 fday, sasats sales from indlyip \
     union all \
     select rowid _id, saitem item, sawhse whse, safyr fyear, safwk fweek, \
     7 fday, sasuns sales from indlyip',
     [analysis.get_gregorian_date]
).build()
 
