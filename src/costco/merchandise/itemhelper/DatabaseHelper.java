package costco.merchandise.itemhelper;

import java.io.File;
import android.database.sqlite.SQLiteDatabase;

public class DatabaseHelper {
	public SQLiteDatabase database = SQLiteDatabase.openOrCreateDatabase(
		new File("/Removable/MicroSD/merch/sales.db"), null
	);

}
