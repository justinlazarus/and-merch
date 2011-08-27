import builders
import analysis

builders.AvailableViews().drop()
builders.AvailableViews().create()

builders.AndroidMetadata().prepare()

""" VIEW fiscal_years 

Gets the first day of every fiscal year from the information available in 
INFLSHP. This file contains all sales information for every day in the 
region, so it also contains the start date of every fiscal year.

"""
builders.SimpleView(
    'fiscal_years',
    'flash',
    ['inflshp',],
    'select rowid _id, flfyr fiscal_year, fldate start_date from (select \
    distinct flfyr, fldate from inflshp where flper=1 and flweek=1 and flday=1)'
).build()

""" VIEW item_basics

Basic information about our items including description, inventory on hand, 
price and department. 

"""
builders.SimpleView(
    'item_basics',
    'item',
    ['inwitmp', 'incatdp', 'inreptp',],
    'select inwitmp.rowid _id, wiwhse whs, widept department, wiitem item, \
    wiohun on_hand, \
    wiohrt rtv_on_hand, round(wisell*1.05) price, wistat status, idcat1 cat1, \
    idcat2 \
    cat2, idcat3 cat3, iddes1 description, iddes2 description2, \
    idsgn1 sign_description, idsgn2 sign_description2, cddesc \
    cat_description, irmpk master_pack, irwgt weight, ircube cube \
    from inwitmp inner join incatdp on widept = cddept and idcat1 = cdcat1 \
    and idcat2 = cdcat2 and idcat3 = cdcat3 inner join inreptp on \
    wiitem = iritem and wiwhse = irwhse'
).build()

""" VIEW daily_sales 

Packages the information in INDLYIP into a more usable format. Includes 
gregorian dates and the weekly total units sold.

"""
builders.UdfView(
    'daily_sales',
    'item',
    ['indlyip', 'fiscal_years',],
    'select indlyip.rowid _id, sawhse whs, saitem item, safyr fiscal_year, \
     get_fiscal_quarter(safwk) fiscal_quarter, get_fiscal_period(safwk) \
     fiscal_period, safwk fiscal_week,  samons mon, satues tue, saweds wed, \
     sathus thu, safris fri, sasats sat, sasuns sun, \
     get_gregorian_date(start_date, safwk, 1) week_start_date \
     from indlyip inner join fiscal_years on safyr=fiscal_year',  
    [analysis.get_gregorian_date, analysis.get_fiscal_period, 
        analysis.get_fiscal_quarter
    ]
).build()
     
builders.Index(
    'daily_sales_weekly',
    'daily_sales',
    'whs, item, fiscal_year, fiscal_week'
).build()

""" VIEWS daily_sales - average week by year, quarter, period

Building off the daily_sales view, this view runs an aggregate function over a 
grouping of the sales over the entire year. The results are a row for every 
item in the daily_sales view. Each column in this row is the adjusted average
sales for that day. For more information on how the adjusted average function 
works, see class AdjustedAverage in the analysis module. 
 
"""
builders.UdfView(
    'daily_sales_yearly_average', 
    'item',
    ['daily_sales',],
    'select _id, whs, item, fiscal_year, adjustedaverage(mon) mon, \
     adjustedaverage(tue) tue, \
     adjustedaverage(wed) wed, adjustedaverage(thu) thu, \
     adjustedaverage(fri) fri, adjustedaverage(sat) sat, \
     adjustedaverage(sun) sun \
     from daily_sales group by item, whs, fiscal_year',
    [],
    [analysis.AdjustedAverage]
).build()

builders.Index(
    'daily_sales_yearly_average_primary',
    'daily_sales_yearly_average',
    'whs, item, fiscal_year'
).build()

builders.UdfView(
    'daily_sales_quarterly_average', 
    'item',
    ['daily_sales',],
    'select _id, whs, item, fiscal_year, fiscal_quarter, \
     adjustedaverage(mon) mon, \
     adjustedaverage(tue) tue, \
     adjustedaverage(wed) wed, adjustedaverage(thu) thu, \
     adjustedaverage(fri) fri, adjustedaverage(sat) sat, \
     adjustedaverage(sun) sun \
     from daily_sales group by whs, item, fiscal_year, fiscal_quarter',
    [],
    [analysis.AdjustedAverage]
).build()

builders.Index(
    'daily_sales_quarterly_average_primary',
    'daily_sales_quarterly_average',
    'whs, item, fiscal_year, fiscal_quarter'
).build()

builders.UdfView(
    'daily_sales_period_average', 
    'item',
    ['daily_sales',],
    'select _id, whs, item, fiscal_year, fiscal_period, \
     adjustedaverage(mon) mon, \
     adjustedaverage(tue) tue, \
     adjustedaverage(wed) wed, adjustedaverage(thu) thu, \
     adjustedaverage(fri) fri, adjustedaverage(sat) sat, \
     adjustedaverage(sun) sun \
     from daily_sales group by whs, item, fiscal_year, fiscal_period',
    [],
    [analysis.AdjustedAverage]
).build()

builders.Index(
    'daily_sales_period_average_primary',
    'daily_sales_period_average',
    'whs, item, fiscal_year, fiscal_period'
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
builders.UdfView(
    'weekly_sales',
    'item',
    ['inihstp',],
    ' '.join(
        ['select rowid _id, ihwhse whs, ihdept department, ihitem item, \
        ihfyr fiscal_year, get_fiscal_quarter(%s) fiscal_quarter, \
        get_fiscal_period(%s) fiscal_period, %s fiscal_week, \
        ihs$%02d sales, ihsu%02d units \
        from inihstp union all' % 
        (week, week, week, week, week) for week in range(1,53)] 
    ) + ' select rowid _id, ihwhse whs, ihdept department, ihitem item, \
        ihfyr fiscal_year, get_fiscal_quarter(53) fiscal_quarter, \
        get_fiscal_period(53) fiscal_period, 53 fiscal_week, ihs$53 sales, \
        ihsu53 units \
        from inihstp',
        [analysis.get_fiscal_quarter, analysis.get_fiscal_period]
).build()

builders.Index(
    'weekly_sales_daily',
    'weekly_sales',
    'whs, item, fiscal_year, fiscal_week'
).build()

""" VIEWS - weekly sales yearly, quarterly and period averages.

Average over the sales and unit values in the weekly_sales view. 

"""
builders.UdfView(
    'weekly_sales_yearly_average',
    'item',
    ['weekly_sales',],
    'select _id, whs, item, fiscal_year, \
    adjustedaverage(sales) average_sales, \
    adjustedaverage(units) average_units \
    from weekly_sales group by whs, item, fiscal_year',
    [],
    [analysis.AdjustedAverage]
).build()

builders.Index(
    'weekly_sales_yearly_average_primary',
    'weekly_sales_yearly_average',
    'whs, item, fiscal_year'
).build()

builders.UdfView(
    'weekly_sales_quarterly_average',
    'item',
    ['weekly_sales',],
    'select _id, whs, item, fiscal_year, fiscal_quarter, \
    adjustedaverage(sales) average_sales, \
    adjustedaverage(units) average_units \
    from weekly_sales group by whs, item, fiscal_year, fiscal_quarter',
    [],
    [analysis.AdjustedAverage]
).build()

builders.Index(
    'weekly_sales_quarterly_average_primary',
    'weekly_sales_quarterly_average',
    'whs, item, fiscal_year, fiscal_quarter'
).build()

builders.UdfView(
    'weekly_sales_period_average',
    'item',
    ['weekly_sales',],
    'select _id, whs, item, fiscal_year, fiscal_quarter, fiscal_period, \
    adjustedaverage(sales) average_sales, \
    adjustedaverage(units) average_units \
    from weekly_sales group by whs, item, fiscal_year, fiscal_period',
    [],
    [analysis.AdjustedAverage]
).build()

builders.Index(
    'weekly_sales_period_average_primary',
    'weekly_sales_period_average',
    'whs, item, fiscal_year, fiscal_period'
).build()
