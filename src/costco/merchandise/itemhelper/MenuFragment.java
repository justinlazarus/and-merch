package costco.merchandise.itemhelper;

import android.app.FragmentTransaction;
import android.app.ListFragment;
import android.database.Cursor;
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
	String [] currentFilters;
	
	@Override 
	public void onActivityCreated(Bundle savedInstanceState) {
		super.onActivityCreated(savedInstanceState);
		setHasOptionsMenu(true);
		Cursor mCursor = new DatabaseHelper().database.rawQuery("select * from avl_views", null);
		ListAdapter mAdapter = new SimpleCursorAdapter(
			getActivity(), android.R.layout.two_line_list_item, mCursor, 
			new String[] {"name", "table"}, 
			new int[] {android.R.id.text1, android.R.id.text2}
		);
		
		setListAdapter(mAdapter);
		getListView().setChoiceMode(ListView.CHOICE_MODE_SINGLE);
	}
	
	@Override 
	public void onListItemClick(ListView parentListView, View selectedView, int position, long id) {
		showDetails(selectedView, position, id);
	}
	
	@Override 
	public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
		MenuItem item = menu.add("Search");
		item.setIcon(android.R.drawable.ic_menu_search);
		item.setShowAsAction(MenuItem.SHOW_AS_ACTION_IF_ROOM);
		SearchView sv = new SearchView(getActivity());
		sv.setIconified(false);
		sv.setOnQueryTextListener(this);
		item.setActionView(sv);
	}
	
	@Override 
	public boolean onQueryTextSubmit(String query) {
		return true;
	}
	
	public boolean onQueryTextChange(String newText) {
		String filter = !TextUtils.isEmpty(newText) ? newText : null;
		currentFilters[0] = filter;
        return true;
    }

	void showDetails(View selectedView, int position, long id) {	
		getListView().setItemChecked(position, true);
		TextView listItemTableName = (TextView) selectedView.findViewById(android.R.id.text2);
		String tableName = listItemTableName.getText().toString();
		DetailFragment detail = DetailFragment.newInstance(tableName, currentFilters);
		FragmentTransaction ft = getFragmentManager().beginTransaction();
		ft.replace(R.id.details_frame, detail);
		ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_FADE);
		ft.commit();
	}
}