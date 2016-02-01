package com.vandenrobotics.functionfirst.tabs;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import com.vandenrobotics.functionfirst.views.NumberPicker;
import android.widget.ToggleButton;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.activities.MatchActivity;
import com.vandenrobotics.functionfirst.model.AutoData;

/**
 * Created by Programming701-A on 12/11/2014.
 */
public class AutoFragment extends Fragment {

    private MatchActivity mActivity;
    private boolean viewsAssigned = false;

    public AutoData mAutoData;

    private CheckBox hadAuto;
    private NumberPicker totesToAuto;
    private NumberPicker containersToAuto;
    private NumberPicker containersFromStep;
    private NumberPicker totesFromStep;
    private ToggleButton[] autoStack;
    private CheckBox endInAuto;
    private CheckBox hadOther;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
        View rootView = inflater.inflate(R.layout.fragment_auto, container, false);
        mActivity = (MatchActivity) getActivity();

        mAutoData = mActivity.mMatchData.mAutoData;

        if(viewsAssigned) loadData(mAutoData);

        return rootView;
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState){
        super.onViewCreated(view, savedInstanceState);
        assignViews(view);
        if(viewsAssigned) loadData(mAutoData);
    }

    @Override
    public void onPause(){
        super.onPause();
        mAutoData = new AutoData(saveData());
        mActivity.mMatchData.mAutoData = mAutoData;
        viewsAssigned=false;
    }

    @Override
    public void onResume(){
        super.onResume();
        assignViews(getView());
        if(viewsAssigned) loadData(mAutoData);
    }

    public void loadData(final AutoData autoData){
        // take the autoData and assign it to each view
        hadAuto.setChecked(autoData.hadAuto);
        totesToAuto.setValue(autoData.totesToAuto);
        containersToAuto.setValue(autoData.containersToAuto);
        containersFromStep.setValue(autoData.containersFromStep);
        totesFromStep.setValue(autoData.totesFromStep);
        for(int i = 0; i < autoStack.length; i++){
            autoStack[i].setChecked(autoData.autoStack[i]);
        }
        endInAuto.setChecked(autoData.endInAuto);
        hadOther.setChecked(autoData.hadOther);

        if(hadAuto.isChecked())
            enableAutoViews();
        else
            disableAutoViews();
    }

    public AutoData saveData(){
        AutoData autoData = new AutoData();
        if(viewsAssigned){
            autoData.hadAuto = hadAuto.isChecked();
            autoData.totesToAuto = totesToAuto.getValue();
            autoData.containersToAuto = containersToAuto.getValue();
            autoData.containersFromStep = containersFromStep.getValue();
            autoData.totesFromStep = totesFromStep.getValue();
            for(int i = 0; i < autoData.autoStack.length; i++){
                autoData.autoStack[i] = autoStack[i].isChecked();
            }
            autoData.endInAuto = endInAuto.isChecked();
            autoData.hadOther = hadOther.isChecked();
        }

        return autoData;
    }

    private void assignViews(View view){
        try{
            // assign all the custom view info to their respective views in the xml
            hadAuto = (CheckBox)view.findViewById(R.id.cb_hadAuto);
            totesToAuto = (NumberPicker)view.findViewById(R.id.pickerTotesToAuto);
            containersToAuto = (NumberPicker)view.findViewById(R.id.pickerContainersToAuto);
            containersFromStep = (NumberPicker)view.findViewById(R.id.pickerContainersFromStep);
            totesFromStep = (NumberPicker)view.findViewById(R.id.pickerTotesFromStep);
            autoStack = new ToggleButton[3];
            autoStack[0] = (ToggleButton)view.findViewById(R.id.toggleAutoStackBase);
            autoStack[1] = (ToggleButton)view.findViewById(R.id.toggleAutoStackMid);
            autoStack[2] = (ToggleButton)view.findViewById(R.id.toggleAutoStackTop);
            endInAuto = (CheckBox)view.findViewById(R.id.cb_endInAuto);
            hadOther = (CheckBox)view.findViewById(R.id.cb_hadOther);

            hadAuto.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v){
                    if(hadAuto.isChecked())
                        enableAutoViews();
                    else
                        disableAutoViews();
                }
            });

            totesToAuto.setMinValue(0);
            totesToAuto.setMaxValue(3);
            containersToAuto.setMinValue(0);
            containersToAuto.setMaxValue(7);
            containersFromStep.setMinValue(0);
            containersFromStep.setMaxValue(4);
            totesFromStep.setMinValue(0);
            totesFromStep.setMaxValue(12);

            viewsAssigned = true;
        } catch (Exception e){
            e.printStackTrace();
            viewsAssigned = false;
        }
    }

    private void enableAutoViews(){
        totesToAuto.setEnabled(true);
        containersToAuto.setEnabled(true);
        containersFromStep.setEnabled(true);
        totesFromStep.setEnabled(true);
        for(ToggleButton tb : autoStack){
            tb.setEnabled(true);
        }
        endInAuto.setEnabled(true);
        hadOther.setEnabled(true);
    }

    private void disableAutoViews(){
        totesToAuto.setValue(0);
        totesToAuto.setEnabled(false);
        containersToAuto.setValue(0);
        containersToAuto.setEnabled(false);
        containersFromStep.setValue(0);
        containersFromStep.setEnabled(false);
        totesFromStep.setValue(0);
        totesFromStep.setEnabled(false);
        for(ToggleButton tb : autoStack){
            tb.setChecked(false);
            tb.setEnabled(false);
        }
        endInAuto.setChecked(false);
        endInAuto.setEnabled(false);
        hadOther.setChecked(false);
        hadOther.setEnabled(false);
    }
}
