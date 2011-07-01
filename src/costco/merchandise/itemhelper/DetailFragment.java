package costco.merchandise.itemhelper;

import java.io.File;

import android.app.ListFragment;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListAdapter;
import android.widget.SimpleCursorAdapter;

public class DetailFragment extends ListFragment {
	
	View detailListHeader;
	
	public static DetailFragment newInstance(String tableName, int rowLayout, int rowHeader, String searchFilter) {
		DetailFragment fragment = new DetailFragment();
		Bundle fragmentArgs = new Bundle();
		fragmentArgs.putString("table", tableName);
		fragmentArgs.putInt("row_layout", rowLayout);
		fragmentArgs.putInt("row_header", rowHeader);
		fragmentArgs.putString("search_filter", searchFilter);
		fragment.setArguments(fragmentArgs);
		return fragment;
	}
	
	public String getSelectedTable() {
		return getArguments().getString("table");
	}
	
	public int getSelectedRowLayout() {
		return getArguments().getInt("row_layout");
	}
	
	public int getSelectedRowHeader() {
		return getArguments().getInt("row_header");
	}
	
	public String getSearchFilter() {
		return getArguments().getString("search_filter");
	}
	
	@Override public void onActivityCreated(Bundle savedInstanceState) {
		super.onActivityCreated(savedInstanceState);
		
		File dbfile = new File("/Removable/MicroSD/merch/sales.db");
		SQLiteDatabase db = SQLiteDatabase.openOrCreateDatabase(dbfile, null);
		Cursor detailCursor = db.rawQuery("select * from " + getSelectedTable() + " where item = " + getSearchFilter() + " order by fyear desc, fweek desc", null);
		
		ListAdapter detailAdapter = new SimpleCursorAdapter(getActivity(), getSelectedRowLayout(),detailCursor, DailySalesView.fromFields,DailySalesView.toFields);
		this.getListView().addHeaderView(detailListHeader);
		setListAdapter(detailAdapter);
	}
	
	@Override public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View detailList = inflater.inflate(R.layout.detail_fragment, container, false);
		detailListHeader = inflater.inflate(getSelectedRowHeader(), null, false);
		return detailList;
	}
}
