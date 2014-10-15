and-merch
=========

Android application to view item and sales information

This application was created to allow a merchandise manager quick access 
to sales and inventory information on a cell phone using any Android 
operating system. 

Data import process:
  - Locate required DB2 files on the iSeries and export to .csv files 
  based on established view defs
  
  - Using any available methods to run python on Android, execute 
  Legacy.create() 
  
  - Legacy.create() will load all .csv rows into appropriate sqlite 
  tables and views
  
Android Application:
  There are 2 main views in the android application. 
  
  - Item Information
  Shows basic item information for an item keyed in the search field.

  - Sales Information
  Shows sales information for items, locations, categories and departments.
