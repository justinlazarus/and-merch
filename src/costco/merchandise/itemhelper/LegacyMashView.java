package costco.merchandise.itemhelper;

import android.app.Activity;
import android.database.Cursor;
import android.widget.ListAdapter;
import android.widget.SimpleCursorAdapter;

public class LegacyMashView {
	private String[] fromFields;
	private int[] toFields; 
	private int rowLayout;
	
	public ListAdapter getListAdapter(
		String tableName, String [] searchFilters, Activity activity
	) {
		Cursor mCursor = new DatabaseHelper().database.rawQuery(
			"select * from " + tableName + " where item = ?", searchFilters 
		);
		ListAdapter mAdapter = new SimpleCursorAdapter(
			activity, rowLayout, mCursor, fromFields, toFields
		);
		return mAdapter;
	}
}