package com.vandenrobotics.ragunasf.controllers.match;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Spinner;
import com.vandenrobotics.ragunasf.R;
import com.vandenrobotics.ragunasf.adapters.MatchListAdapter;
import com.vandenrobotics.ragunasf.adapters.TeamListAdapter;
import com.vandenrobotics.ragunasf.controllers.EventActivity;
import com.vandenrobotics.ragunasf.model.Match;
import com.vandenrobotics.ragunasf.model.ScoutingPosition;
import com.vandenrobotics.ragunasf.model.Team;

public class MatchSetupFragment extends Fragment {

    private EventActivity mActivity;

    private ScoutingPosition mScoutingPosition;
    private Match mMatch;
    private Team mTeam;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_match_setup, container, false);
        mActivity = (EventActivity)getActivity();

        mScoutingPosition = ScoutingPosition.RedTeam1;
        mMatch = mActivity.getEvent().getMatches().get(0);
        mTeam = mMatch.getTeam(mScoutingPosition);

        // Inflate the layout for this fragment
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
            //TODO: add a search bar for the match and team spinners
            // assign all the custom view info to their respective views in the xml
            final EditText mEditText_Matches = (EditText)view.findViewById(R.id.editText_Match);
            final ListView mMatchList = (ListView)view.findViewById(R.id.listView_Matches);
            final EditText mEditText_Teams = (EditText)view.findViewById(R.id.editText_Team);
            final ListView mTeamList = (ListView)view.findViewById(R.id.listView_Teams);
            final Spinner ScoutingPositionSpinner = (Spinner)view.findViewById(R.id.spinner_ScoutingPosition);
            final Button mStartMatchButton = (Button)view.findViewById(R.id.button_StartMatch);

            final MatchListAdapter mMatchListAdapter = new MatchListAdapter(mActivity, mActivity.getEvent().getMatches());
            mMatchList.setTextFilterEnabled(true);
            mMatchList.setAdapter(mMatchListAdapter);
            try{
                if(mMatchList.getCheckedItemCount()>0) {
                    mTeamList.setItemChecked(mTeamList.getCheckedItemPosition(), false);
                }
                mMatchList.setItemChecked(mMatchListAdapter.getPosition(mMatch), true);
                mMatchList.setSelection(mMatchListAdapter.getPosition(mMatch));
            } catch(NullPointerException e){
                e.printStackTrace();
            }

            final TeamListAdapter mTeamListAdapter = new TeamListAdapter(mActivity, mActivity.getEvent().getTeams());
            mTeamList.setTextFilterEnabled(true);
            mTeamList.setAdapter(mTeamListAdapter);
            try{
                if(mTeamList.getCheckedItemCount()>0){
                    mTeamList.setItemChecked(mTeamList.getCheckedItemPosition(), false);
                }

                mTeamList.setItemChecked(mTeamListAdapter.getPosition(mTeam), true);
                mTeamList.setSelection(mTeamListAdapter.getPosition(mTeam));
            } catch(NullPointerException e){
                e.printStackTrace();
            }

            final ArrayAdapter<ScoutingPosition> mPositionsAdapter =
                    new ArrayAdapter<>(mActivity, android.R.layout.simple_list_item_1, ScoutingPosition.values());
            ScoutingPositionSpinner.setAdapter(mPositionsAdapter);
            ScoutingPositionSpinner.setSelection(mPositionsAdapter.getPosition(mScoutingPosition));

            mMatchListAdapter.getFilter().filter(mEditText_Matches.getText().toString());
            mTeamListAdapter.getFilter().filter(mEditText_Teams.getText().toString());

            mEditText_Matches.addTextChangedListener(new TextWatcher() {
                @Override
                public void beforeTextChanged(CharSequence s, int start, int count, int after) {

                }

                @Override
                public void onTextChanged(CharSequence s, int start, int before, int count) {
                    mMatchListAdapter.getFilter().filter(s);
                }

                @Override
                public void afterTextChanged(Editable s) {

                }
            });

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

            ScoutingPositionSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                @Override
                public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                    mScoutingPosition = (ScoutingPosition) ScoutingPositionSpinner.getItemAtPosition(position);
                    ScoutingPositionSpinner.setSelection(position);
                    mTeam = mMatch.getTeam(mScoutingPosition);
                    if(mTeamList.getCheckedItemCount()>0) {
                        mTeamList.setItemChecked(mTeamList.getCheckedItemPosition(), false);
                    }
                    mTeamList.setItemChecked(mTeamListAdapter.getPosition(mTeam), true);
                    mTeamList.setSelection(mTeamListAdapter.getPosition(mTeam));
                }

                @Override
                public void onNothingSelected(AdapterView<?> parent) {
                }
            });

            mMatchList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    mMatchList.setItemChecked(position, true);
                    mMatch = (Match) mMatchList.getItemAtPosition(mMatchList.getCheckedItemPosition());
                    mTeam = mMatch.getTeam(mScoutingPosition);
                    if (mTeamList.getCheckedItemCount() > 0) {
                        mTeamList.setItemChecked(mTeamList.getCheckedItemPosition(), false);
                    }
                    mTeamList.setItemChecked(mTeamListAdapter.getPosition(mTeam), true);
                    mTeamList.setSelection(mTeamListAdapter.getPosition(mTeam));
                }
            });

            mTeamList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    if(mTeamList.getCheckedItemCount()>0) {
                        mTeamList.setItemChecked(mTeamList.getCheckedItemPosition(), false);
                    }
                    mTeamList.setItemChecked(position, true);
                    mTeam = (Team) mTeamList.getItemAtPosition(mTeamList.getCheckedItemPosition());
                }
            });

            mStartMatchButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (mMatch != null && mTeam != null) {
                        startActivity(new Intent(mActivity, MatchScoutActivity.class));
                    }
                }
            });

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
