import sqlite3
import settings
import legacy
import inspect

class View: 
    def __init__(
        self, table_name, view_group, required_tables, select,
        udf_list=None, agg_list=None
    ):
        self.con = sqlite3.connect(settings.DB_PATH)
        self.cur = self.con.cursor()
        self.table_name = table_name
        self.view_group = view_group
        self.required_tables = required_tables
        self.select = select
        self.udf_list = udf_list
        self.agg_list = agg_list
   
    def build(self):
        for table in self.required_tables:
            if legacy.Table(table).exists():
                continue
            else:
                return None

        for udf in self.udf_list:
            num_args = len(inspect.getargspec(udf)[0]) - 1
            self.con.create_function(udf.__name__.lower(), num_args, udf)
                
        for agg in self.agg_list:
            num_args = len(inspect.getargspec(agg.step)[0]) - 1
            self.con.create_aggregate(agg.__name__.lower(), num_args, agg)

        if (self.udf_list or self.agg_list): 
            self.cur.execute('drop table if exists %s' % (self.table_name))
            self.cur.execute(
                'create table %s as %s' % (self.table_name, self.select)
            )
        else:
            self.con.execute('drop view if exists %s' % (name))
            self.con.execute('create view %s as %s' % (name, select))

        # Add the just created view to the table of available views
        self.cur.execute(
            'create table if not exists available_views \
             (_id int primary key autoincrement not null, name text, type text)'
        )
        self.cur.execute(
            'insert into available views (name, type) values (%s, %s)' %
             (view_name, view_type)
        ) 
