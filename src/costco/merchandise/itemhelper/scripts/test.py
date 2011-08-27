import builders
import analysis 

builders.UdfView(
    'new_daily',
    'item',
    ['indlyip',],

    'select indlyip.rowid _id, saitem item, sawhse whs, safyr fiscal_year, \
     safwk fiscal_week, 1 day_of_week, samons sales, \
     get_gregorian_date(start_date, safwk, 1) date \
     from indlyip inner join fiscal_years on safyr = fiscal_year \
     union all \
     select indlyip.rowid _id, saitem item, sawhse whs, safyr fiscal_year, \
     safwk fiscal_week, 2 day_of_week, samons sales, \
     get_gregorian_date(start_date, safwk, 2) date \
     from indlyip inner join fiscal_years on safyr = fiscal_year \
     union all \
     select indlyip.rowid _id, saitem item, sawhse whs, safyr fiscal_year, \
     safwk fiscal_week, 3 day_of_week, samons sales, \
     get_gregorian_date(start_date, safwk, 3) date \
     from indlyip inner join fiscal_years on safyr = fiscal_year \
     union all \
     select indlyip.rowid _id, saitem item, sawhse whs, safyr fiscal_year, \
     safwk fiscal_week, 4 day_of_week, samons sales, \
     get_gregorian_date(start_date, safwk, 4) date \
     from indlyip inner join fiscal_years on safyr = fiscal_year \
     union all \
     select indlyip.rowid _id, saitem item, sawhse whs, safyr fiscal_year, \
     safwk fiscal_week, 5 day_of_week, samons sales, \
     get_gregorian_date(start_date, safwk, 5) date \
     from indlyip inner join fiscal_years on safyr = fiscal_year \
     union all \
     select indlyip.rowid _id, saitem item, sawhse whs, safyr fiscal_year, \
     safwk fiscal_week, 6 day_of_week, samons sales, \
     get_gregorian_date(start_date, safwk, 6) date \
     from indlyip inner join fiscal_years on safyr = fiscal_year \
     union all \
     select indlyip.rowid _id, saitem item, sawhse whs, safyr fiscal_year, \
     safwk fiscal_week, 7 day_of_week, samons sales, \
     get_gregorian_date(start_date, safwk, 7) date \
     from indlyip inner join fiscal_years on safyr = fiscal_year',
     [analysis.get_gregorian_date]
).build()

builders.Index(
    'new_daily_natural',
    'new_daily',
    'whs, item, fiscal_year, fiscal_week'
).build()    
