package costco.merchandise.itemhelper;

import android.app.ListFragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class DetailFragment extends ListFragment {
	
	public static DetailFragment newInstance(String tableName, String [] searchFilters) {
		DetailFragment fragment = new DetailFragment();
		Bundle fragmentArgs = new Bundle();
		fragmentArgs.putString("table", tableName);
		fragmentArgs.putStringArray("search_filters", searchFilters);
		fragment.setArguments(fragmentArgs);
		return fragment;
	}
	
	private String getSelectedTable() {
		return getArguments().getString("table");
	}
	
	private String [] getSearchFilters() {
		return getArguments().getStringArray("search_filters");
	}
	
	@Override 
	public void onActivityCreated(Bundle savedInstanceState) {
		super.onActivityCreated(savedInstanceState);
		setListAdapter(new DailySalesView().getListAdapter(getSearchFilters(), getActivity()));
	}
	
	@Override 
	public View onCreateView(
		LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState
	) {
		View detailList = inflater.inflate(R.layout.detail_fragment, container, false);
		return detailList;
	}
}
