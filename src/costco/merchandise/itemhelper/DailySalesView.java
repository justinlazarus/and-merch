package costco.merchandise.itemhelper;

import android.app.Activity;
import android.database.Cursor;
import android.widget.ListAdapter;
import android.widget.SimpleCursorAdapter;

public class DailySalesView {
	private String[] fromFields = {"fyear", "fweek", "total_week", "m", "t","w","th","f","sa","su"};
	private int[] toFields = {
		R.id.year, R.id.week, R.id.total_units, R.id.monday_units, 
		R.id.tuesday_units, R.id.wednesday_units, R.id.thursday_units, 
		R.id.friday_units, R.id.saturday_units, R.id.sunday_units
	};
	private int rowLayout = R.layout.daily_sales;
	private String [] filters;
	private Activity activity;
	
	public DailySalesView(String [] searchFilters, Activity parentActivity) {
		filters = searchFilters;
		activity = parentActivity;
	}
	
	public ListAdapter getListAdapter() {
		Cursor mCursor = new DatabaseHelper().database.rawQuery(
			"select * from daily_sales where item = ? order by fyear desc, " +
			"fweek desc", filters 
		);
		ListAdapter mAdapter = new SimpleCursorAdapter(
			activity, rowLayout, mCursor, fromFields, toFields
		);
		return mAdapter;
	}
}