import sqlite3
import math
import inspect
import pdb

DB_LOCATION = '/home/justin/merch/sales.db'

class TableBuilder: 
    def __init__(self):
        self.con = sqlite3.connect(DB_LOCATION)
        self.cur = self.con.cursor()
   
    def build(self, name, select, udf_list = [], aggregate_list = []):
        for udf in udf_list:
            num_args = len(inspect.getargspec(udf)[0])
            self.con.create_function(udf.__name__.lower(), num_args, udf)
                
        for agg in aggregate_list:
            num_args = len(inspect.getargspec(agg.step)[0]) - 1
            self.con.create_aggregate(agg.__name__.lower(), num_args, agg)

        self.cur.execute('drop table if exists %s' % (name))
        self.cur.execute('create table %s as %s' % (name, select))

class ViewBuilder:
    def __init__(self):
        self.con = sqlite3.connect(DB_LOCATION)
        self.cur = self.con.cursor()
 
    def build(self, name, select):
        self.cur.execute('drop view if exists %s' % (name))
        self.cur.execute('create view %s as %s' % (name, select))

class AdjustedAverage:
    """ Implements the adjustedaverage sqlite user defined ag function.
 
    step() -- invoked on every permutation of the aggregate query. In this 
    case step simply appends the current value to the list of values.

    finalize() -- called once at the end of every group of records. Finalize
    removes any outliers from the data set and then takes the average. 
 
    """
    def __init__(self):
        self.values = []
 
    def step(self, value):
        self.values.append(value)
 
    def finalize(self):
        sales = SalesAnalysis(self.values)        
        sales.remove_outliers()
        return sales.get_average()
 
class SalesAnalysis:
    """ Analyzes sales data. 
 
    values -- stores the list of sales values to be analyzed.  
    remove_outliers() -- removes outliers from the sales data. 
    get_average() -- returns the calculated average of the sales data. 
    percentile() -- returns a percentile boundary of the sales data.
    get_bounds() -- returns the upper and lower outlier boundaries of the data.

    """
    def __init__(self, values):
        self.values = values

    def remove_outliers(self):
        if self.values:
            upper, lower = self.get_bounds()
            self.values = [x for x in self.values if (x < upper and x > lower)]
    
    def get_average(self):
        if not self.values:
            return None

        return sum(self.values) / len(self.values)
 
    def percentile(self, percent, key=lambda x:x):
        if not self.values:
            return None

	k = (len(self.values) - 1) * percent
	f = math.floor(k)
	c = math.ceil(k)
	if f == c:
	    return key(self.values[int(k)])

	d0 = key(self.values[int(f)]) * (k-f)
	d1 = key(self.values[int(c)]) * (c-k)
	return d0 + d1

    def get_bounds(self):
        self.values.sort()
        seventy_fifth = self.percentile(0.75)
        twenty_fifth = self.percentile(0.25)
        fourth_spread = seventy_fifth - twenty_fifth
        median = self.percentile(0.5)
        upper_bound = median + (1.5 * fourth_spread)
        lower_bound = median - (1.5 * fourth_spread)
        return (upper_bound, lower_bound)
