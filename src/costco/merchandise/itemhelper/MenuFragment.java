package costco.merchandise.itemhelper;

import java.io.File;

import android.app.FragmentTransaction;
import android.app.ListFragment;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SearchView;
import android.widget.SearchView.OnQueryTextListener;
import android.widget.SimpleCursorAdapter;
import android.widget.TextView;

public class MenuFragment extends ListFragment implements OnQueryTextListener {
	String currentFilter;
	
	@Override public void onActivityCreated(Bundle savedInstanceState) {
		
		super.onActivityCreated(savedInstanceState);
		
		setHasOptionsMenu(true);
		
		File dbfile = new File("/Removable/MicroSD/merch/sales.db");
		SQLiteDatabase db = SQLiteDatabase.openOrCreateDatabase(dbfile, null);
		Cursor viewsCursor = db.rawQuery("select * from avl_views", null);
		
		ListAdapter mAdapter = new SimpleCursorAdapter(getActivity(), android.R.layout.two_line_list_item,
				viewsCursor, new String[] {"name", "table"}, new int[] {android.R.id.text1, android.R.id.text2});
		
		setListAdapter(mAdapter);
		getListView().setChoiceMode(ListView.CHOICE_MODE_SINGLE);
	}
	
	@Override public void onListItemClick(ListView parentListView, View selectedView, int position, long id) {
		showDetails(selectedView, position, id);
	}
	
	@Override public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
		MenuItem itemDescription = menu.add("Item Description");
		itemDescription.setShowAsAction(MenuItem.SHOW_AS_ACTION_IF_ROOM);
		TextView tv = new TextView(getActivity());
		tv.setTag("item_description");
		tv.setId(666);
		itemDescription.setActionView(tv);
		
		MenuItem item = menu.add("Search");
		item.setIcon(android.R.drawable.ic_menu_search);
		item.setShowAsAction(MenuItem.SHOW_AS_ACTION_IF_ROOM);
		SearchView sv = new SearchView(getActivity());
		sv.setIconified(false);
		sv.setOnQueryTextListener(this);
		item.setActionView(sv);
	}
	
	@Override public boolean onQueryTextSubmit(String query) {
		return true;
	}
	
	public boolean onQueryTextChange(String newText) {
		currentFilter = !TextUtils.isEmpty(newText) ? newText : null;
        return true;
    }

	void showDetails(View selectedView, int position, long id) {	
		
		// Get table name from listView selection
		getListView().setItemChecked(position, true);
		TextView listItemTableName = (TextView) selectedView.findViewById(android.R.id.text2);
		String tableName = listItemTableName.getText().toString();
		
		// Get fragment info
		DetailFragment detail = (DetailFragment) getFragmentManager().findFragmentByTag("detail_fragment");
		int[] layouts = getLayouts(tableName);
		detail = DetailFragment.newInstance(tableName, layouts[0], layouts[1], currentFilter);
		
		// Update the action bar with the item description
		File dbfile = new File("/Removable/MicroSD/merch/sales.db");
		SQLiteDatabase db = SQLiteDatabase.openOrCreateDatabase(dbfile, null);
		Cursor itemCursor = db.rawQuery("select * from inwitmp where wiitem = " + currentFilter, null);
		itemCursor.moveToNext();
		TextView tv = (TextView) getActivity().findViewById(666);
		tv.setText(itemCursor.getString(12) + " (" + itemCursor.getString(15) + ") ON HAND: " + itemCursor.getString(3) + " PRICE: $" + Math.round(itemCursor.getInt(6) * 1.05));
		
		// Fade in the detail fragment
		FragmentTransaction ft = getFragmentManager().beginTransaction();
		ft.replace(R.id.details_frame, detail);
		ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_FADE);
		ft.commit();
	}
	
	int [] getLayouts(String tableName) {
		int[] layouts;
		layouts = new int [2];
		if (tableName.equals("daily_sales")) {
			layouts[0] = R.layout.daily_sales;
			layouts[1] = R.layout.daily_sales_header;
		}
		if (tableName.equals("avg_daily_sales")) {
			layouts[0] = R.layout.daily_sales;
			layouts[1] = R.layout.daily_sales_header;
		}
		return layouts;
	}
}