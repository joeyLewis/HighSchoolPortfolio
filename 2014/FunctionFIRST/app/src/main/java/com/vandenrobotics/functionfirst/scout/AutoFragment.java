package com.vandenrobotics.functionfirst.scout;

import com.vandenrobotics.functionfirst.R;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.InputDevice;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.NumberPicker;
import android.widget.NumberPicker.OnValueChangeListener;

import com.vandenrobotics.functionfirst.scout.model.AutoData;

public class AutoFragment extends Fragment {

	private CheckBox autoHadAuto;
	private CheckBox autoMobilityBonus;
	private CheckBox autoGoalieZone;
	
	private NumberPicker autoHighScore;
	private NumberPicker autoLowScore;
	
	private CheckBox[] autoHighHot = new CheckBox[3];
	
	private CheckBox[] autoLowHot = new CheckBox[3];
	
	private boolean viewsAssigned = false;
	
	private boolean waitLeft = false;
	private boolean waitRight = false;
	
	private AutoData mAutoData;
	
	public static AutoFragment newInstance(AutoData autoData){
		AutoFragment af = new AutoFragment();
		
		Bundle args = new Bundle();
		args.putParcelable("AutoData",autoData);
		
		af.setArguments(args);
		
		return af;
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
							 Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.fragment_scout_auto, container, false);
		
		Bundle args = getArguments();
		mAutoData = args.getParcelable("AutoData");
		
		if(viewsAssigned) loadData(mAutoData);
		
		return rootView;
	}
	
	@Override
	public void onViewCreated(View view, Bundle savedInstanceState){
		super.onViewCreated(view, savedInstanceState);
		assignViews(view);
		loadData(mAutoData);
	}
	
	@Override
	public void setUserVisibleHint(boolean isVisibleToUser) {
		super.setUserVisibleHint(isVisibleToUser);
		if(!viewsAssigned);
		else if(isVisibleToUser)
		{
			loadData(mAutoData);
		}
		else if(!isVisibleToUser)
		{
			saveData(mAutoData);
		}
	}
	
	@Override
	public void onPause(){
		super.onPause();
		saveData(mAutoData);
		viewsAssigned=false;
	}
	
	@Override
	public void onResume(){
		super.onResume();
		assignViews(getView());
	}
	
	private void loadData(final AutoData autoData){
		autoHadAuto.setChecked(autoData.hadAuto);
		autoMobilityBonus.setChecked(autoData.mobilityBonus);
		autoGoalieZone.setChecked(autoData.goalieZone);
		autoHighScore.setValue(autoData.highScore);
		autoLowScore.setValue(autoData.lowScore);
		autoHighHot[0].setChecked(autoData.highHot[0]);
		autoHighHot[1].setChecked(autoData.highHot[1]);
		autoHighHot[2].setChecked(autoData.highHot[2]);
		autoLowHot[0].setChecked(autoData.lowHot[0]);
		autoLowHot[1].setChecked(autoData.lowHot[1]);
		autoLowHot[2].setChecked(autoData.lowHot[2]);
		
		if(autoHadAuto.isChecked())
			enableAutoViews();
		else
			disableAutoViews();
	}
	
	private void saveData(AutoData autoData){
		if(viewsAssigned){
			autoData.hadAuto = autoHadAuto.isChecked();
			autoData.mobilityBonus = autoMobilityBonus.isChecked();
			autoData.goalieZone = autoGoalieZone.isChecked();
			autoData.highScore = autoHighScore.getValue();
			autoData.lowScore = autoLowScore.getValue();
			autoData.highHot[0] = autoHighHot[0].isChecked();
			autoData.highHot[1] = autoHighHot[1].isChecked();
			autoData.highHot[2] = autoHighHot[2].isChecked();
			autoData.lowHot[0] = autoLowHot[0].isChecked();
			autoData.lowHot[1] = autoLowHot[1].isChecked();
			autoData.lowHot[2] = autoLowHot[2].isChecked();
		}
	}
	
	private void assignViews(View view){
		try{
			autoHadAuto = (CheckBox)view.findViewById(R.id.autoHadAuto);
			autoMobilityBonus = (CheckBox)view.findViewById(R.id.autoMobilityBonus);
			autoGoalieZone = (CheckBox)view.findViewById(R.id.autoGoalieZone);
			
			autoHighScore = (NumberPicker)view.findViewById(R.id.autoHighScore);
			autoHighScore.setMinValue(0);
			autoHighScore.setMaxValue(3);
			autoLowScore = (NumberPicker)view.findViewById(R.id.autoLowScore);
			autoLowScore.setMinValue(0);
			autoLowScore.setMaxValue(3);
			
			autoHighHot[0] = (CheckBox)view.findViewById(R.id.autoHighHot1);
			autoHighHot[1] = (CheckBox)view.findViewById(R.id.autoHighHot2);
			autoHighHot[2] = (CheckBox)view.findViewById(R.id.autoHighHot3);
			
			autoLowHot[0] = (CheckBox)view.findViewById(R.id.autoLowHot1);
			autoLowHot[1] = (CheckBox)view.findViewById(R.id.autoLowHot2);
			autoLowHot[2] = (CheckBox)view.findViewById(R.id.autoLowHot3);
			
			autoHadAuto.setOnClickListener(new View.OnClickListener() {
				
				@Override
				public void onClick(View v) {
					if(autoHadAuto.isChecked())
						enableAutoViews();
					else
						disableAutoViews();
					
				}
			});
			
			autoHighScore.setOnValueChangedListener(new OnValueChangeListener() {
	
				@Override
				public void onValueChange(NumberPicker arg0, int oldVal, int newVal) {
					// if oldVal is greater than newVal, change the checkbox value to false
					if(oldVal>newVal && oldVal != 0)
						autoHighHot[oldVal-1].setChecked(false);
					
					// disable everything that was enabled before
					for(int i = 0; i < oldVal; i++){
						autoHighHot[i].setEnabled(false);
						autoHighHot[i].setTextColor(getResources().getColor(R.color.Gray));
					}
					
					// enable everything that should be enabled now
					for(int i = 0; i < newVal; i++){
						autoHighHot[i].setEnabled(true);
						autoHighHot[i].setTextColor(getResources().getColor(R.color.Black));
					}
				}
			});
			
			autoLowScore.setOnValueChangedListener(new OnValueChangeListener() {
	
				@Override
				public void onValueChange(NumberPicker arg0, int oldVal, int newVal) {
					// if oldVal is greater than newVal, change the checkbox value to false
					if(oldVal>newVal && oldVal != 0)
						autoLowHot[oldVal-1].setChecked(false);
					
					// disable everything that was enabled before
					for(int i = 0; i < oldVal; i++){
						autoLowHot[i].setEnabled(false);
						autoLowHot[i].setTextColor(getResources().getColor(R.color.Gray));
					}
					
					// enable everything that should be enabled now
					for(int i = 0; i < newVal; i++){
						autoLowHot[i].setEnabled(true);
						autoLowHot[i].setTextColor(getResources().getColor(R.color.Black));
					}
				}
			});
		
			viewsAssigned = true;
		} catch (Exception e){
			e.printStackTrace();
			viewsAssigned = false;
		}
	}
	
	private void disableAutoViews(){
		autoMobilityBonus.setChecked(false);
		autoMobilityBonus.setEnabled(false);
		autoMobilityBonus.setTextColor(getResources().getColor(R.color.Gray));
		autoHighScore.setValue(0);
		autoHighScore.setEnabled(false);
		autoLowScore.setValue(0);
		autoLowScore.setEnabled(false);
		for(int i = 0; i < 3; i++){
			autoHighHot[i].setChecked(false);
			autoHighHot[i].setEnabled(false);
			autoHighHot[i].setTextColor(getResources().getColor(R.color.Gray));
			autoLowHot[i].setChecked(false);
			autoLowHot[i].setEnabled(false);
			autoLowHot[i].setTextColor(getResources().getColor(R.color.Gray));
		}
	}
	
	private void enableAutoViews(){
		autoMobilityBonus.setEnabled(true);
		autoMobilityBonus.setTextColor(getResources().getColor(R.color.Black));
		autoHighScore.setEnabled(true);
		autoLowScore.setEnabled(true);
		for(int i = 0; i < autoHighScore.getValue(); i++){
			autoHighHot[i].setEnabled(true);
			autoHighHot[i].setTextColor(getResources().getColor(R.color.Black));
		}
		for(int i = 0; i < autoLowScore.getValue(); i++){
			autoLowHot[i].setEnabled(true);
			autoLowHot[i].setTextColor(getResources().getColor(R.color.Black));
		}
	}
	
	public boolean onMyKeyDown(int keyCode){
		switch(keyCode) {
		case KeyEvent.KEYCODE_BUTTON_Y:
			autoHadAuto.toggle();
			if(autoHadAuto.isChecked())
				enableAutoViews();
			else
				disableAutoViews();
			return true;
		case KeyEvent.KEYCODE_BUTTON_X:
			if(autoHadAuto.isChecked())
				autoMobilityBonus.toggle();
			return true;
		case KeyEvent.KEYCODE_BUTTON_B:
			autoGoalieZone.toggle();
			return true;
		case KeyEvent.KEYCODE_BUTTON_THUMBL:
			if(autoHadAuto.isChecked()){
				try {
					autoHighHot[autoHighScore.getValue()-1].toggle();
				} catch (IndexOutOfBoundsException e){
					e.printStackTrace();
				}
			}
			return true;
		case KeyEvent.KEYCODE_BUTTON_THUMBR:
			if(autoHadAuto.isChecked()){
				try {
					autoLowHot[autoLowScore.getValue()-1].toggle();
				} catch (IndexOutOfBoundsException e){
					e.printStackTrace();
				}
			}
			return true;
		default:
			return true;
		}
	}
	
	public boolean onMyGenericMotionEvent(MotionEvent event){
		if(autoHadAuto.isChecked()){
			if((event.getSource() & InputDevice.SOURCE_JOYSTICK) == InputDevice.SOURCE_JOYSTICK){
				switch(event.getAction()){
				case 2: // either joystick, reading off for some reason
					if(event.getAxisValue(MotionEvent.AXIS_Y)<0.25 &&
							event.getAxisValue(MotionEvent.AXIS_Y)>-0.25){
						waitLeft = false;
					}
					if(event.getAxisValue(MotionEvent.AXIS_RZ)<0.25 &&
							event.getAxisValue(MotionEvent.AXIS_RZ)>-0.25){
						waitRight = false;
					}
					
					int oldVal = autoHighScore.getValue();
					if(!waitLeft){
						if(event.getAxisValue(MotionEvent.AXIS_Y)>0.75){
							autoHighScore.setValue(autoHighScore.getValue()-1);
							waitLeft = true;
						}
						else if(event.getAxisValue(MotionEvent.AXIS_Y)<-0.75){
							autoHighScore.setValue(autoHighScore.getValue()+1);
							waitLeft = true;
						}
					}
					
					int newVal = autoHighScore.getValue();
					
					if(oldVal>newVal && oldVal != 0)
						autoHighHot[oldVal-1].setChecked(false);
					
					// disable everything that was enabled before
					for(int i = 0; i < oldVal; i++){
						autoHighHot[i].setEnabled(false);
						autoHighHot[i].setTextColor(getResources().getColor(R.color.Gray));
					}
					
					// enable everything that should be enabled now
					for(int i = 0; i < newVal; i++){
						autoHighHot[i].setEnabled(true);
						autoHighHot[i].setTextColor(getResources().getColor(R.color.Black));
					}
					
					oldVal = autoLowScore.getValue();
					if(!waitRight){
						if(event.getAxisValue(MotionEvent.AXIS_RZ)>0.75){
							autoLowScore.setValue(autoLowScore.getValue()-1);
							waitRight = true;
						}
						else if(event.getAxisValue(MotionEvent.AXIS_RZ)<-0.75){
							autoLowScore.setValue(autoLowScore.getValue()+1);
							waitRight = true;
						}
					}
					
					newVal = autoLowScore.getValue();
					
					if(oldVal>newVal && oldVal != 0)
						autoLowHot[oldVal-1].setChecked(false);
					
					// disable everything that was enabled before
					for(int i = 0; i < oldVal; i++){
						autoLowHot[i].setEnabled(false);
						autoLowHot[i].setTextColor(getResources().getColor(R.color.Gray));
					}
					
					// enable everything that should be enabled now
					for(int i = 0; i < newVal; i++){
						autoLowHot[i].setEnabled(true);
						autoLowHot[i].setTextColor(getResources().getColor(R.color.Black));
					}
					return true;
					
				default:
					return false;
				}
			}
		}
		return false;
	}
}
