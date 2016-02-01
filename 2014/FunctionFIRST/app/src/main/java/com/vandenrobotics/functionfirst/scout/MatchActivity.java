package com.vandenrobotics.functionfirst.scout;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.adapter.TabsPagerAdapter;
import com.vandenrobotics.functionfirst.adapter.TabsViewPager;
import com.vandenrobotics.functionfirst.scout.model.MatchData;

import com.vandenrobotics.functionfirst.scout.AutoFragment;
import com.vandenrobotics.functionfirst.scout.TeleFragment;
import com.vandenrobotics.functionfirst.scout.PostFragment;

import android.app.ActionBar;
import android.app.ActionBar.Tab;
import android.app.AlertDialog;
import android.app.FragmentTransaction;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.NavUtils;
import android.support.v4.view.PagerTabStrip;
import android.support.v4.view.ViewPager;
import android.text.InputType;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

public class MatchActivity extends FragmentActivity 
	implements ActionBar.TabListener {

	private TabsViewPager viewPager;
	private TabsPagerAdapter mAdapter;
	private ActionBar actionBar;
	
	private MatchData mMatchData;
	private int teamNumber;
	private int curMatch;
	private int deviceNumber;
	private int allianceColor;
	private int textColor;
	
	private TextView initTeamNumber;
	private TextView initMatchNumber;
	private TextView initDeviceNumber;
	private PagerTabStrip initAllianceColor;

	// Tab titles
	private final String[] tabs = {"Autonomous", "Tele-Op", "Post Match"};
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_match);
		// Initialization
		teamNumber = getIntent().getIntExtra("teamNumber",701); // default is our team :)
		curMatch = getIntent().getIntExtra("matchNumber",ScoutActivity.mCurMatch);
		deviceNumber = getIntent().getIntExtra("deviceNumber",0);
		allianceColor = (deviceNumber>0 && deviceNumber<4)? R.color.FIRST_red : R.color.FIRST_blue;
		textColor = (allianceColor==R.color.FIRST_red)? R.color.Black : R.color.White;
		viewPager = (TabsViewPager) findViewById(R.id.pager);
		actionBar = getActionBar();
		
		setupInitBar();
		
		actionBar.setHomeButtonEnabled(false);
		actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);
		
		// Adding Tabs
		for (String tab_name : tabs) {
			actionBar.addTab(actionBar.newTab().setText(tab_name)
					.setTabListener(this));
		
		setupActionBar();
		
		}

		viewPager.setOnPageChangeListener(new ViewPager.OnPageChangeListener(){
		
			@Override
			public void onPageSelected(int position){
				// on changing the page
				// make respected tab selected
				actionBar.setSelectedNavigationItem(position);
			}
			
			@Override
			public void onPageScrolled(int arg0, float arg1, int arg2){
			}
			
			@Override
			public void onPageScrollStateChanged(int arg0){
			}		
		});
	}
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.scout, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case android.R.id.home:
			// This ID represents the Home or Up button. In the case of this
			// activity, the Up button is shown. Use NavUtils to allow users
			// to navigate up one level in the application structure. For
			// more details, see the Navigation pattern on Android Design:
			//
			// http://developer.android.com/design/patterns/navigation.html#up-vs-back
			//
			NavUtils.navigateUpFromSameTask(this);
			return true;
		case R.id.action_go_to_match:
			final AlertDialog.Builder builder = new AlertDialog.Builder(this);
			final EditText input = new EditText(this);
			input.setRawInputType(InputType.TYPE_CLASS_NUMBER);
			input.setHint("Enter a number between 1 and "+ScoutActivity.maxMatches+".");
			builder.setTitle("Go To Match:")
				   .setView(input)
				   .setPositiveButton(R.string.accept,new DialogInterface.OnClickListener(){
					   public void onClick(DialogInterface dialog, int id) {
						   try{
							   int match = Integer.parseInt(input.getText().toString());
							   goToMatch(match,deviceNumber);
						   } catch (NumberFormatException e){
							   e.printStackTrace();
						   }
					   }
				   })
				   .setNegativeButton(R.string.cancel,new DialogInterface.OnClickListener(){
					   public void onClick(DialogInterface dialog, int id){
					   }
				   });
				   builder.show();
			return true;
		case R.id.action_set_device:
			final AlertDialog.Builder builder2 = new AlertDialog.Builder(this);
			final EditText input2 = new EditText(this);
			input2.setHint("Enter a number between 1 and 6.");
			input2.setRawInputType(InputType.TYPE_CLASS_NUMBER);
			builder2.setTitle("Set Device Number:")
				   .setView(input2)
				   .setPositiveButton(R.string.accept,new DialogInterface.OnClickListener(){
					   public void onClick(DialogInterface dialog, int id) {
						   try{
							   int dNum = Integer.parseInt(input2.getText().toString());
							   if(dNum>0 && dNum<7){
								   goToMatch(curMatch, dNum);
							   }
						   } catch (NumberFormatException e){
							   e.printStackTrace();
						   }
					   }
				   })
				   .setNegativeButton(R.string.cancel,new DialogInterface.OnClickListener(){
					   public void onClick(DialogInterface dialog, int id){
					   }
				   });
				   builder2.show();
			return true;
		}
		return super.onOptionsItemSelected(item);
	}
	
	private void setupActionBar() {
		if(getActionBar() != null) getActionBar().setDisplayHomeAsUpEnabled(true);

	}
	
	private void setupInitBar(){
		initTeamNumber = (TextView)findViewById(R.id.initTeamNumber);
		initTeamNumber.setText("Team: " + teamNumber);
		initTeamNumber.setTextColor(getResources().getColor(textColor));
		initMatchNumber = (TextView)findViewById(R.id.initMatchNumber);
		initMatchNumber.setText("Match: " + curMatch);
		initMatchNumber.setTextColor(getResources().getColor(textColor));
		initDeviceNumber = (TextView)findViewById(R.id.initDeviceNumber);
		initDeviceNumber.setText("Device Number: " + deviceNumber);
		initDeviceNumber.setTextColor(getResources().getColor(textColor));
		initAllianceColor = (PagerTabStrip)findViewById(R.id.pager_title_strip);
		initAllianceColor.setDrawFullUnderline(true);
		initAllianceColor.setTabIndicatorColor(getResources().getColor(allianceColor));
		initAllianceColor.setBackgroundColor(getResources().getColor(allianceColor));
	}
	
	@Override
	protected void onPause(){		
		super.onPause();
		
		getSupportFragmentManager().
		findFragmentByTag("android:switcher:" 
						   + R.id.pager + ":" 
						   + viewPager.getCurrentItem()).onPause();

		if(deviceNumber == ScoutActivity.deviceNumber){
			// save team number, match number, and alliance color
			ScoutActivity.mMatchResults[curMatch-1] = mMatchData;
			ScoutActivity.mCurMatch = curMatch;
			
			// over-write data to file
			ScoutActivity.writeData();
			ScoutActivity.writeMatch(curMatch);
		}
	}
	
	@Override
	protected void onResume(){
		super.onResume();
			
		if(ScoutActivity.mMatchResults[curMatch-1] != null)
		{
			mMatchData = ScoutActivity.mMatchResults[curMatch-1];
		}
		else
		{
			mMatchData = new MatchData();
			mMatchData.initData.matchNumber = curMatch;
			mMatchData.initData.teamNumber = teamNumber;
			mMatchData.initData.allianceColor = (deviceNumber>0&&deviceNumber<4)? 0 : 1;
		}
				
		mAdapter = new TabsPagerAdapter(getSupportFragmentManager(),
				mMatchData.autoData,mMatchData.teleData,mMatchData.postData);
		
		viewPager.setAdapter(mAdapter);
		actionBar.setSelectedNavigationItem(viewPager.getCurrentItem());
	}
	
	public void goTo_nextMatch(View view){
		// pause all fragments in order to save the data from them
		for(int i = 0; i < 3; i++)
			getSupportFragmentManager().
				findFragmentByTag("android:switcher:" 
								   + R.id.pager + ":" 
								   + i).onPause();
		startActivity(ScoutActivity.goToMatch(this,curMatch,curMatch+1,deviceNumber,mMatchData));
		this.finish();
	}
	
	private void goToMatch(int match, int dNum){
		startActivity(ScoutActivity.goToMatch(this,curMatch,match,dNum,mMatchData));
		this.finish();
	}
	
	@Override
	public void onTabReselected(Tab tab, FragmentTransaction ft) {
	}

	@Override
	public void onTabSelected(Tab tab, FragmentTransaction ft) {
		// set the tab bar to the current tab
		viewPager.setCurrentItem(tab.getPosition());
	}

	@Override
	public void onTabUnselected(Tab tab, FragmentTransaction ft) {
	}
	
	@Override
	public boolean onKeyDown(int keyCode, KeyEvent event){
		if(keyCode == KeyEvent.KEYCODE_BUTTON_R1 ||
				keyCode == KeyEvent.KEYCODE_BUTTON_R2){
			viewPager.setCurrentItem(viewPager.getCurrentItem()+1);
			actionBar.setSelectedNavigationItem(viewPager.getCurrentItem());
			return true;
		}
		if(keyCode == KeyEvent.KEYCODE_BUTTON_L1 ||
				keyCode == KeyEvent.KEYCODE_BUTTON_L2){
			viewPager.setCurrentItem(viewPager.getCurrentItem()-1);
			actionBar.setSelectedNavigationItem(viewPager.getCurrentItem());
			return true;
		}
		else{
			switch(viewPager.getCurrentItem()){
			case 0:
				return ((AutoFragment) getSupportFragmentManager().
							findFragmentByTag("android:switcher:" 
								   + R.id.pager + ":0" )).onMyKeyDown(keyCode);
			case 1:
				return ((TeleFragment) getSupportFragmentManager().
						findFragmentByTag("android:switcher:" 
							   + R.id.pager + ":1" )).onMyKeyDown(keyCode);
			case 2:
				return ((PostFragment) getSupportFragmentManager().
						findFragmentByTag("android:switcher:" 
							   + R.id.pager + ":2" )).onMyKeyDown(keyCode);
			default:
				return super.onKeyDown(keyCode, event);
			}
		}
	}
	
	@Override
	public boolean onGenericMotionEvent(MotionEvent event){
		switch(viewPager.getCurrentItem()){
		case 0:
			return ((AutoFragment) getSupportFragmentManager().
						findFragmentByTag("android:switcher:" 
							   + R.id.pager + ":0" )).onMyGenericMotionEvent(event);
		case 2:
			return ((PostFragment) getSupportFragmentManager().
					findFragmentByTag("android:switcher:" 
						   + R.id.pager + ":2" )).onMyGenericMotionEvent(event);
		default:
			return super.onGenericMotionEvent(event);
		}
	}
}
