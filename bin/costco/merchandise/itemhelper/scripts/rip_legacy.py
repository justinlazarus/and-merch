import legacy 
import settings
import os

# Import legacy tables from .csv files on the MicroSD card
os.chdir(settings.IMPORT_PATH)
dirlist = os.listdir(settings.IMPORT_PATH)

for entry in dirlist:
    entry_name, entry_extension = os.path.splitext(entry)
    if entry_extension == '.csv':
        legacy.Table(entry, settings.ENCODING, entry_name).create()
