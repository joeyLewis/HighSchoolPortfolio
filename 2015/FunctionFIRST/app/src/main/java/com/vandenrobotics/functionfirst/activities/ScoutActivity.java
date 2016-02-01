package com.vandenrobotics.functionfirst.activities;

import android.view.View;
import android.widget.AdapterView;
import android.widget.Spinner;
import android.widget.EditText;
import android.widget.ArrayAdapter;
import android.content.Intent;
import android.app.Activity;
import android.os.Bundle;

import android.widget.TextView;
import android.view.inputmethod.EditorInfo;
import android.view.KeyEvent;
import android.view.inputmethod.InputMethodManager;
import android.content.Context;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.model.Match;
import com.vandenrobotics.functionfirst.model.MatchData;
import com.vandenrobotics.functionfirst.tools.ExternalStorageTools;
import com.vandenrobotics.functionfirst.tools.JSONTools;
import com.vandenrobotics.functionfirst.views.NumberPicker;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;

public class ScoutActivity extends Activity {

    private String mEvent;
    private int mDeviceNumber;
    private int mCurMatch;
    private int mTeamNumber;
    private ArrayList<Integer> team_numbers;

    private ArrayList<Match> mMatchList;
    private ArrayList<MatchData> mMatchData;

    private Spinner spinnerDevices;
    private ArrayAdapter<CharSequence> deviceAdapter;
    private NumberPicker pickerMatches;
    private Spinner spinnerTeams;
    private ArrayAdapter<Integer> teamAdapter;

    private final int MAX_MATCHES = 200; // a reasonable amount of matches to expect any event to have less than

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scout);
        mEvent = getIntent().getStringExtra("event");
        mDeviceNumber = ExternalStorageTools.readDevice(mEvent);
        mCurMatch = ExternalStorageTools.readCurrentMatch(mEvent, mDeviceNumber);
        mMatchList = ExternalStorageTools.readMatches(mEvent);
        mMatchData = ExternalStorageTools.readData(mEvent, mDeviceNumber);

        ArrayList<JSONObject> teamInfo = ExternalStorageTools.readTeams(mEvent);
        teamInfo = JSONTools.sortJSONArray(teamInfo, "team_number");
        team_numbers = new ArrayList<>(teamInfo.size());
        try {
            for (int i = 0; i < teamInfo.size(); i++) {
                team_numbers.add(i, teamInfo.get(i).getInt("team_number"));
            }
        } catch (JSONException e){
            e.printStackTrace();
        }
        Collections.sort(team_numbers);

        spinnerDevices = (Spinner)findViewById(R.id.spinnerDeviceNumber);
        deviceAdapter = ArrayAdapter.createFromResource(this, R.array.deviceOptions, R.layout.spinner_base);
        deviceAdapter.setDropDownViewResource(R.layout.spinner_dropdown);
        spinnerDevices.setAdapter(deviceAdapter);
        spinnerDevices.setSelection(mDeviceNumber-1);

        pickerMatches = (NumberPicker)findViewById(R.id.pickerMatch);
        pickerMatches.setMinValue(1);
        pickerMatches.setMaxValue(MAX_MATCHES);
        pickerMatches.setValue(mCurMatch);

        spinnerTeams = (Spinner)findViewById(R.id.spinnerTeamNumber);
        teamAdapter = new ArrayAdapter<>(this, R.layout.spinner_base, team_numbers);
        teamAdapter.setDropDownViewResource(R.layout.spinner_dropdown);
        spinnerTeams.setAdapter(teamAdapter);
        spinnerTeams.setSelection(teamAdapter.getPosition(mTeamNumber));

        spinnerDevices.setOnItemSelectedListener(new Spinner.OnItemSelectedListener(){
            @Override
            public void onItemSelected(AdapterView<?> adapter, View v, int position, long arg3) {
                mDeviceNumber=spinnerDevices.getSelectedItemPosition()+1;
                mCurMatch = ExternalStorageTools.readCurrentMatch(mEvent, mDeviceNumber);
                mTeamNumber = (mMatchList.size()>0)? mMatchList.get(mCurMatch-1).teams[mDeviceNumber - 1] : 0;

                pickerMatches.setValue(mCurMatch);
                spinnerTeams.setSelection(teamAdapter.getPosition(mTeamNumber));
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapter){

            }
        });

        spinnerTeams.setOnItemSelectedListener(new Spinner.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapter, View v, int position, long arg3) {
                mTeamNumber = Integer.parseInt(spinnerTeams.getItemAtPosition(position).toString());
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapter) {

            }
        });
    }

    public void activityMatch(View view){
        // load the new match, passing all the info to it
        mDeviceNumber = spinnerDevices.getSelectedItemPosition()+1;
        ExternalStorageTools.writeDevice(mDeviceNumber, mEvent);
        mCurMatch = pickerMatches.getValue();
        ExternalStorageTools.writeCurrentMatch(mCurMatch, mEvent, mDeviceNumber);
        mTeamNumber = (int)spinnerTeams.getSelectedItem();
        Intent intent = new Intent(this, MatchActivity.class);
        try {
            intent.putExtra("event", mEvent);
            intent.putExtra("matchNumber", mCurMatch);
            intent.putExtra("teamNumber", mTeamNumber);
            intent.putExtra("deviceNumber", mDeviceNumber);
            intent.putExtra("matchData", mMatchData);
        } catch (IndexOutOfBoundsException e){
            e.printStackTrace();
        }
        startActivity(intent);
        this.finish();
    }
}
