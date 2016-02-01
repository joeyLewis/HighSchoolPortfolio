package com.vandenrobotics.functionfirst.tabs;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import com.vandenrobotics.functionfirst.views.NumberPicker;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.activities.MatchActivity;
import com.vandenrobotics.functionfirst.model.PostData;

/**
 * Created by Programming701-A on 12/11/2014.
 */
public class PostFragment extends Fragment {

    private MatchActivity mActivity;
    private boolean viewsAssigned = false;

    private NumberPicker numFouls;
    private CheckBox gotRedCard;
    private CheckBox gotYellowCard;
    private CheckBox wasDisabled;

    private PostData mPostData;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
        View rootView = inflater.inflate(R.layout.fragment_post, container, false);
        mActivity = (MatchActivity) getActivity();

        mPostData = mActivity.mMatchData.mPostData;

        if(viewsAssigned) loadData(mPostData);

        return rootView;
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState){
        super.onViewCreated(view, savedInstanceState);
        assignViews(view);
        if(viewsAssigned) loadData(mPostData);
    }

    @Override
    public void onPause(){
        super.onPause();
        mPostData = new PostData(saveData());
        mActivity.mMatchData.mPostData = mPostData;
        viewsAssigned=false;
    }

    @Override
    public void onResume(){
        super.onResume();
        assignViews(getView());
        if(viewsAssigned) loadData(mPostData);
    }

    public void loadData(final PostData postData){
        // take the postData and assign it to each view
        numFouls.setValue(postData.numFouls);
        gotRedCard.setChecked(postData.gotRedCard);
        gotYellowCard.setChecked(postData.gotYellowCard);
        wasDisabled.setChecked(postData.wasDisabled);
    }

    public PostData saveData(){
        PostData postData = new PostData();
        if(viewsAssigned){
            postData.numFouls = numFouls.getValue();
            postData.gotRedCard = gotRedCard.isChecked();
            postData.gotYellowCard = gotYellowCard.isChecked();
            postData.wasDisabled = wasDisabled.isChecked();
        }

        return postData;
    }

    private void assignViews(View view){
        try{
            // assign all the custom view info to their respective views in the xml
            numFouls = (NumberPicker)view.findViewById(R.id.pickerNumFouls);
            gotRedCard = (CheckBox)view.findViewById(R.id.cb_gotRedCard);
            gotYellowCard = (CheckBox)view.findViewById(R.id.cb_gotYellowCard);
            wasDisabled = (CheckBox)view.findViewById(R.id.cb_wasDisabled);

            numFouls.setMinValue(0);
            numFouls.setMaxValue(999);

            viewsAssigned = true;
        } catch (Exception e){
            e.printStackTrace();
            viewsAssigned = false;
        }
    }
}
