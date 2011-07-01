package costco.merchandise.itemhelper;

import android.app.Activity;
import android.app.FragmentTransaction;
import android.os.Bundle;

public class MainActivity extends Activity {
	
	@Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main_activity);

        // Add the SQL view selection fragment to the menu frame
        MenuFragment menuList = new MenuFragment();
        final FragmentTransaction ft = getFragmentManager().beginTransaction();
        ft.add(R.id.menu_list_frame, menuList, "menu_fragment");
        ft.commit();        
    }
}
