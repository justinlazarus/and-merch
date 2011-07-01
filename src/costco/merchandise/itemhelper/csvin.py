import csv
import codecs
import sqlite3

class CSVTable(object):
    def __init__(self, csv_file, csv_encoding):
        self.csvreader = CSVReader(csv_file, csv_encoding)
        
    def create(self, filepath, tablename):
        self.con = sqlite3.connect(filepath)
        self.con.text_factory = str
        self.tablename = tablename
        self.con.execute('drop table if exists %s' % tablename)
        
        self.fieldnames = self._get_fieldnames(tablename)

        for row in self.csvreader:
            if self.csvreader.reader.line_num==1:
                self._create_table(row)
                continue

            self._save_data(row)

        self.con.commit()
 
    def _create_table(self, row):
        namestypes = zip(
            self.fieldnames, [self._get_type(field) for field in row]
        )
        self.con.execute(
            'create table %s (%s)' % ( 
                self.tablename, ','.join(
                    ['"%s" %s' % nametype for nametype in namestypes]
                )
            )
        )   
        self._save_data(row)

    def _get_fieldnames(self, tablename):
        fieldnames = []

        file_definition = open(''.join((tablename, '.fdf')))
        for line in file_definition:
            if line.startswith('PCFL'):
                fieldnames.append(line[5:line.find(' ', 5)])
            else: 
                continue

        return fieldnames

    def _get_type(self, field):
        try:
            int(field)
            return 'int'
        except ValueError:
            return 'text'

    def _save_data(self, row):
        if row == []:
            return

        query = """insert into %s values(%s)""" % (
            self.tablename,
            ','.join(['?' for field in row])
        )
        self.con.execute(query, row)
            
class CSVReader(object):
    def __init__(self, csv_data, csv_encoding, **kwds):
        self.reader = csv.reader(
            self.encode_utf_8(open(csv_data), csv_encoding)
        )

    def __iter__(self):
        return self.reader

    def next(self):
        row = self.reader.__next__()
        return [field for field in row]
 
    def encode_utf_8(self, csv_data, csv_encoding):
        for line in csv_data:
            try: 
                yield line.decode(csv_encoding).encode('utf-8')
            except UnicodeDecodeError:
                next
