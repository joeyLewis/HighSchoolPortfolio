package com.vandenrobotics.functionfirst.adapter;

import com.vandenrobotics.functionfirst.scout.*;
import com.vandenrobotics.functionfirst.scout.model.AutoData;
import com.vandenrobotics.functionfirst.scout.model.TeleData;
import com.vandenrobotics.functionfirst.scout.model.PostData;

import android.support.v4.app.FragmentManager;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentPagerAdapter;

public class TabsPagerAdapter extends FragmentPagerAdapter {

	private AutoData mAutoData;
	private TeleData mTeleData;
	private PostData mPostData;
	
	public TabsPagerAdapter(FragmentManager fm, 
			AutoData autoData, TeleData teleData, PostData postData){
		super(fm);
		mAutoData = autoData;
		mTeleData = teleData;
		mPostData = postData;
	}
	
	@Override
	public Fragment getItem(int index){
		
		switch (index) {
		case 0:
			// autonomous fragment activity
			return AutoFragment.newInstance(mAutoData);
		case 1:
			// tele-op fragment activity
			return TeleFragment.newInstance(mTeleData);
		case 2:
			// post game fragment activity
			return PostFragment.newInstance(mPostData);
		}
		return null;
	}

	@Override
	public int getCount(){
		// returns number of tabs
		return 3;
	}

}
