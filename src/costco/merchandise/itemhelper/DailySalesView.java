package costco.merchandise.itemhelper;

public class DailySalesView {
	public static String[] fromFields = {"fyear", "fweek", "total_week", "m","t","w","th","f","sa","su",};
	public static int[] toFields = {R.id.year, R.id.week, R.id.total_units, R.id.monday_units, R.id.tuesday_units, R.id.wednesday_units, R.id.thursday_units, 
		R.id.friday_units, R.id.saturday_units, R.id.sunday_units};
}
