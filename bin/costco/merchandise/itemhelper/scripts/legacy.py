import settings
import csv
import codecs
import sqlite3

class Table:
    """ A table ripped directly from the iSeries DB2 database via .csv

    create() -- creates a local version of the DB2 table in an sqlite 
    database. Expexts a .csv file for the data and an .fdf file for the 
    field definitions. 

    exists() -- returns True if a table exists in the local database, false
    otherwise. 
 
    """
    def __init__(self, csv_file=None, csv_encoding=None, table_name=None):
        if (csv_file and csv_encoding):
            self.csvreader = Reader(csv_file, csv_encoding)

        self.table_name = table_name
        self.con = sqlite3.connect(settings.DB_PATH)
        self.con.text_factory = str
        
    def create(self):
        """ Creates and populates a new sqlite table.
      
        Using the values in the .csv file and the field defs in the .fdf file,
        this method creates a new sqlite table and populates it with the 
        values in the .csv table. It effectively copies a DB2 table to an 
        sqlite table. 

        """
        print('building table %s...' % self.table_name)
        self.con.execute('drop table if exists %s' % (self.table_name))
        self.fieldnames = self._get_fieldnames()
        self._create_table(self.csvreader.next())
        self._save_data(None, self.csvreader)
        self.con.commit()

    def exists(self):
        """ Returns True if table exists, false otherwise. """ 
        if self.con.execute(
            "select name from sqlite_master where name='%s'" % (self.table_name)
        ).fetchone():
            return True
        else:
            return False 

    def _create_table(self, row):
        """ Creates a new sqlite table""" 
        namestypes = zip(
            self.fieldnames, [self._get_type(field) for field in row]
        )
        self.replacement_list = ','.join(['?' for field in row])
        self.con.execute(
            'create table %s (%s)' % ( 
                self.table_name, ','.join(
                    ['"%s" %s' % nametype for nametype in namestypes]
                )
            )
        )   
        self._save_data(row)

    def _get_fieldnames(self):
        """ Uses the information in the field def file to get fieldnames. """ 
        fieldnames = []

        file_definition = open(''.join((self.table_name, '.fdf')))
        for line in file_definition:
            if line.startswith('PCFL'):
                fieldnames.append(line[5:line.find(' ', 5)])
            else: 
                continue

        return fieldnames

    def _get_type(self, field):
        """ Guesses field type based on results of type casting. """ 
        try:
            int(field)
            return 'int'
        except ValueError:
            return 'text'

    def _save_data(self, row=None, rows=None):
        """ Inserts .csv data into newly created sqlite tables. """
        query = """insert into %s values(%s)""" % (
            self.table_name, self.replacement_list
        )
        if row: 
            self.con.execute(query, row)
        elif rows:
            self.con.executemany(query, rows)
            
class Reader:
    def __init__(self, csv_data, csv_encoding, **kwds):
        self.reader = csv.reader(
            self.encode_utf_8(open(csv_data), csv_encoding)
        )

    def __iter__(self):
        return self.reader

    def next(self):
        row = self.reader.next()
        return [field for field in row]

    def encode_utf_8(self, csv_data, csv_encoding):
        for line in csv_data:
            try: 
                yield line.decode(csv_encoding).encode('utf-8')
            except UnicodeDecodeError:
                next
