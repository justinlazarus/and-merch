package costco.merchandise.itemhelper;

import android.app.Activity;
import android.database.Cursor;
import android.widget.ListAdapter;
import android.widget.SimpleCursorAdapter;

public class DailySalesView extends LegacyMashView {
	public DailySalesView() {
		super();
	}
	
	fromFields = {"fyear", "fweek", "total_week", "m", "t","w","th","f","sa","su"};
	toFields = {
		R.id.year, R.id.week, R.id.total_units, R.id.monday_units, 
		R.id.tuesday_units, R.id.wednesday_units, R.id.thursday_units, 
		R.id.friday_units, R.id.saturday_units, R.id.sunday_units
	};
	private int rowLayout = R.layout.daily_sales;
}