package costco.merchandise.itemhelper;

import android.content.Context;
import android.database.Cursor;
import android.view.View;
import android.widget.SimpleCursorAdapter;

public class DetailListAdapter extends SimpleCursorAdapter {

	public DetailListAdapter(Context context, int layout, Cursor c, String[] from, int[] to) {
		super(context, layout, c, from, to);
	}

	public View getView() {
		return null;
	}
}
