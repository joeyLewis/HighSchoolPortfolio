package com.vandenrobotics.ragunasf.controllers.pits;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;

import com.vandenrobotics.ragunasf.R;
import com.vandenrobotics.ragunasf.adapters.TeamListAdapter;
import com.vandenrobotics.ragunasf.controllers.EventActivity;
import com.vandenrobotics.ragunasf.model.Team;


public class PitSetupFragment extends Fragment {

    private EventActivity mActivity;

    private Team mTeam;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_pit_setup, container, false);
        mActivity = (EventActivity)getActivity();

        return rootView;
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState){
        super.onViewCreated(view, savedInstanceState);
        assignViews(view);
    }

    @Override
    public void onPause(){
        super.onPause();
    }

    @Override
    public void onResume(){
        super.onResume();
        assignViews(getView());
    }

    private void assignViews(View view) {
        try {
            final EditText mEditText_Teams = (EditText)view.findViewById(R.id.editText_PitTeam);
            final ListView mTeamList = (ListView)view.findViewById(R.id.listView_PitTeams);
            final Button mViewEntryButton = (Button)view.findViewById(R.id.button_ViewPitEntry);

            final TeamListAdapter mTeamListAdapter = new TeamListAdapter(mActivity, mActivity.getEvent().getTeams());

            mTeamList.setTextFilterEnabled(true);
            mTeamList.setAdapter(mTeamListAdapter);

            mTeamListAdapter.getFilter().filter(mEditText_Teams.getText().toString());

            try{
                mTeamList.setItemChecked(mTeamListAdapter.getPosition(mTeam), true);
                mTeamList.setSelection(mTeamListAdapter.getPosition(mTeam));
            } catch (NullPointerException e){
                e.printStackTrace();
            }

            mEditText_Teams.addTextChangedListener(new TextWatcher() {
                @Override
                public void beforeTextChanged(CharSequence s, int start, int count, int after) {

                }

                @Override
                public void onTextChanged(CharSequence s, int start, int before, int count) {
                    mTeamListAdapter.getFilter().filter(s);
                }

                @Override
                public void afterTextChanged(Editable s) {

                }
            });

            mTeamList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override

                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    mTeamList.setItemChecked(mTeamList.getCheckedItemPosition(), false);
                    mTeamList.setItemChecked(position, true);
                    mTeam = (Team) mTeamList.getItemAtPosition(mTeamList.getCheckedItemPosition());
                }
            });

            mViewEntryButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (mTeam != null) {
                        startActivity(new Intent(mActivity, PitScoutActivity.class));
                    }
                }
            });

        }
        catch(Exception e){

            e.printStackTrace();
        }
    }
}