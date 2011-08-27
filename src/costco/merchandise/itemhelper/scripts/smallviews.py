import builders
import analysis

builders.AvailableViews().drop()
builders.AvailableViews().create()

""" VIEW fiscal_years 

Gets the first day of every fiscal year from the information available in 
INFLSHP. This file contains all sales information for every day in the 
region, so it also contains the start date of every fiscal year.

"""
""" VIEW item_basics

Basic information about our items including description, inventory on hand, 
price and department. 

"""
builders.SimpleView(
    'item_basics',
    'item',
    ['inwitmp', 'incatdp', 'inreptp',],
    'select wiwhse whs, widept department, wiitem item, wiohun on_hand, \
    wiohrt rtv_on_hand, wisell price, wistat status, idcat1 cat1, idcat2 \
    cat2, idcat3 cat3, iddes1 description, iddes2 description2, \
    idsgn1 sign_description, idsgn2 sign_description2, cddesc \
    cat_description, irmpk master_pack, irwgt weight, ircube cube \
    from inwitmp inner join incatdp on widept = cddept and idcat1 = cdcat1 \
    and idcat2 = cdcat2 and idcat3 = cdcat3 inner join inreptp on \
    wiitem = iritem and wiwhse = irwhse'
).build()


