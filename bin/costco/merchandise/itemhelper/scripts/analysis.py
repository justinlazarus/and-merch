import math
import sqlite3
import settings
import datetime

def get_gregorian_date(fiscal_year_start, fiscal_week, day_of_week):
    if (fiscal_week > 53 or day_of_week > 7):
        return False
    else:
        start_date = datetime.datetime.strptime(
            str(fiscal_year_start), "%Y%m%d"
        )
        greg_date = start_date + datetime.timedelta(
            weeks = (abs(fiscal_week - 1)), days = (abs(day_of_week - 1))
        )
        return int(greg_date.strftime('%Y%m%d'))

def get_fiscal_period(fiscal_week):
    if (fiscal_week < 1 or fiscal_week > 53):
        return None 
    elif fiscal_week == 53:
        return 13
    else:
        return int(math.ceil(float(fiscal_week) / float(4)))

def get_fiscal_quarter(fiscal_week):
    return int(math.ceil(float(fiscal_week) / float(13)))

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
