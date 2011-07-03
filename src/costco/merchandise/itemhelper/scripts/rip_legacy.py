import legacy 
import settings
import os
import prog

# Import legacy tables from .csv files on the MicroSD card
os.chdir(settings.IMPORT_PATH)
dirlist = os.listdir(settings.IMPORT_PATH)
pbar = prog.ProgressBar(maxval=len(dirlist)).start()
count = 0

for entry in dirlist:
    count +=1
    entry_name, entry_extension = os.path.splitext(entry)
    if entry_extension == '.csv':
        legacy.Table(entry, settings.ENCODING, entry_name).create()
        pbar.update(count)
pbar.finish()
print
