package com.vandenrobotics.functionfirst.activities;

import android.support.v4.app.DialogFragment;
import android.support.v4.app.FragmentActivity;

import android.os.Bundle;
import android.support.v4.app.FragmentTabHost;
import android.support.v4.view.PagerTabStrip;
import android.view.View;
import android.widget.TextView;
import android.content.Intent;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.dialogs.DialogListener;
import com.vandenrobotics.functionfirst.model.MatchData;
import com.vandenrobotics.functionfirst.tabs.*;
import com.vandenrobotics.functionfirst.tools.ExternalStorageTools;

import java.util.ArrayList;

public class MatchActivity extends FragmentActivity implements DialogListener {

    private FragmentTabHost mTabHost;
    private InitFragment mInitFrag;
    private AutoFragment mAutoFrag;
    private TeleFragment mTeleFrag;
    private PostFragment mPostFrag;

    public String mEvent;
    public int mMatchNumber;
    public int mTeamNumber;
    public int mDeviceNumber;
    public ArrayList<MatchData> mMatchDataList;
    public MatchData mMatchData;

    private int allianceColor;
    private int textColor;

    private TextView initTeamNumber;
    private TextView initMatchNumber;
    private TextView initDeviceNumber;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_match);

        mEvent = getIntent().getStringExtra("event");
        mMatchNumber = getIntent().getIntExtra("matchNumber", 1);
        mTeamNumber = getIntent().getIntExtra("teamNumber", 0);
        mDeviceNumber = getIntent().getIntExtra("deviceNumber", 1);
        mMatchDataList = getIntent().getParcelableArrayListExtra("matchData");

        try {
            mMatchData = mMatchDataList.get(mMatchNumber - 1);
        } catch (Exception e){
            e.printStackTrace();
            mMatchData = new MatchData();
            mMatchDataList.add(mMatchNumber-1, mMatchData);
        }

        if(mMatchData == null){
            mMatchData = new MatchData();
        }

        allianceColor = (mDeviceNumber>0 && mDeviceNumber<4)? R.color.FIRST_RED : R.color.FIRST_BLUE;
        textColor = (allianceColor==R.color.FIRST_RED)? R.color.Black : R.color.White;

        setupInfoBar();

        mTabHost = (FragmentTabHost) findViewById(R.id.tabHost);
        mTabHost.setup(this, getSupportFragmentManager(), android.R.id.tabcontent);

        mTabHost.addTab(mTabHost.newTabSpec("tab_init")
                .setIndicator(getResources().getString(R.string.title_initTab), null), InitFragment.class, null);
        mTabHost.addTab(mTabHost.newTabSpec("tab_auto")
                .setIndicator(getResources().getString(R.string.title_autoTab), null), AutoFragment.class, null);
        mTabHost.addTab(mTabHost.newTabSpec("tab_tele")
                .setIndicator(getResources().getString(R.string.title_teleTab), null), TeleFragment.class, null);
        mTabHost.addTab(mTabHost.newTabSpec("tab_post")
                .setIndicator(getResources().getString(R.string.title_postTab), null), PostFragment.class, null);
    }

    private void setupInfoBar(){
        initTeamNumber = (TextView)findViewById(R.id.initTeamNumber);
        initTeamNumber.setText("Team: " + mTeamNumber);
        initTeamNumber.setTextColor(getResources().getColor(textColor));

        initMatchNumber = (TextView)findViewById(R.id.initMatchNumber);
        initMatchNumber.setText("Match: " + mMatchNumber);
        initMatchNumber.setTextColor(getResources().getColor(textColor));

        initDeviceNumber = (TextView)findViewById(R.id.initDeviceNumber);
        String deviceText = (mDeviceNumber>0 && mDeviceNumber<4)? "Red " + mDeviceNumber : "Blue " + (mDeviceNumber-3);
        initDeviceNumber.setText("Device: " + deviceText);
        initDeviceNumber.setTextColor(getResources().getColor(textColor));

        PagerTabStrip allianceColorBar = (PagerTabStrip)findViewById(R.id.pager_title_strip);
        allianceColorBar.setDrawFullUnderline(true);
        allianceColorBar.setTabIndicatorColor(getResources().getColor(allianceColor));
        allianceColorBar.setBackgroundColor(getResources().getColor(allianceColor));

    }

    public void dialog_noShow(View view) {
        if (mInitFrag == null)
            mInitFrag = (InitFragment) getSupportFragmentManager().findFragmentByTag("tab_init");
        mInitFrag.command_noShow(view);
    }

    public void dialog_deleteStack(View view) {
        if (mTeleFrag == null)
            mTeleFrag = (TeleFragment) getSupportFragmentManager().findFragmentByTag("tab_tele");
        mTeleFrag.command_deleteStack(view);
    }

    public void dialog_deleteStepStack(View view) {
        if (mTeleFrag == null)
            mTeleFrag = (TeleFragment) getSupportFragmentManager().findFragmentByTag("tab_tele");
        mTeleFrag.command_deleteStepStack(view);
    }

    public void dialog_editStack(View view) {
        if (mTeleFrag == null)
            mTeleFrag = (TeleFragment) getSupportFragmentManager().findFragmentByTag("tab_tele");
        mTeleFrag.command_editStack(view);
    }

    public void dialog_editStepStack(View view) {
        if (mTeleFrag == null)
            mTeleFrag = (TeleFragment) getSupportFragmentManager().findFragmentByTag("tab_tele");
        mTeleFrag.command_editStepStack(view);
    }

    @Override
    public void onDialogPositiveClick(DialogFragment dialog) {
        if (!dialog.equals(null)) {
            if(mInitFrag!=null) {
                if (dialog.equals(mInitFrag.noShowDF)) {
                    mInitFrag.setNoShow(true);
                    // save all data and close the match'
                    this.finishViaNoShow();
                }
            }
            if(mTeleFrag!=null){
                if (dialog.equals(mTeleFrag.deleteStackDF)) {
                    mTeleFrag.deleteStack();
                } else if (dialog.equals(mTeleFrag.deleteStepStackDF)){
                    mTeleFrag.deleteStepStack();
                } else if (dialog.equals(mTeleFrag.editStackDF)){
                    mTeleFrag.editStack();
                } else if (dialog.equals(mTeleFrag.editStepStackDF)){
                    mTeleFrag.editStepStack();
                }
            }
        }
    }

    @Override
    public void onDialogNegativeClick(DialogFragment dialog) {
        if (!dialog.equals(null)) {
            if (mInitFrag != null) {
                if (dialog.equals(mInitFrag.noShowDF)) {
                    mInitFrag.setNoShow(false);
                }
            }
            if (mTeleFrag != null) {
                if (dialog.equals(mTeleFrag.deleteStackDF)) {
                    // pass through without deleting the stack
                    mTeleFrag.cancelDialog();
                } else if (dialog.equals(mTeleFrag.deleteStepStackDF)){
                    // pass through without deleting the step stack
                    mTeleFrag.cancelDialog();
                } else if (dialog.equals(mTeleFrag.editStackDF)){
                    // do not edit the stack and leave the values the same
                    mTeleFrag.cancelDialog();
                } else if (dialog.equals(mTeleFrag.editStepStackDF)){
                    // do not edit the stack and leave the values the same
                    mTeleFrag.cancelDialog();
                }
            }
        }
    }

    public void finishMatch(View view){
        getSupportFragmentManager().findFragmentByTag("tab_post").onPause();
        mMatchData.mInitData.teamNumber = mTeamNumber;
        mMatchData.mInitData.matchNumber = mMatchNumber;
        mMatchData.mInitData.allianceColor = (mDeviceNumber>0 && mDeviceNumber<4)? 0 : 1;
        mMatchDataList.set(mMatchNumber-1, mMatchData);

        ExternalStorageTools.writeData(mMatchDataList, mEvent, mDeviceNumber);
        ExternalStorageTools.writeCurrentMatch(mMatchNumber+1, mEvent, mDeviceNumber);

        Intent intent = new Intent(this, ScoutActivity.class);
        intent.putExtra("event", mEvent);

        startActivity(intent);
        this.finish();
    }

    public void finishViaNoShow(){
        getSupportFragmentManager().findFragmentByTag("tab_init").onPause();
        mMatchData.mInitData.teamNumber = mTeamNumber;
        mMatchData.mInitData.matchNumber = mMatchNumber;
        mMatchData.mInitData.allianceColor = (mDeviceNumber>0 && mDeviceNumber<4)? 0 : 1;
        mMatchDataList.set(mMatchNumber-1, mMatchData);

        ExternalStorageTools.writeData(mMatchDataList, mEvent, mDeviceNumber);
        ExternalStorageTools.writeCurrentMatch(mMatchNumber+1, mEvent, mDeviceNumber);

        Intent intent = new Intent(this, ScoutActivity.class);
        intent.putExtra("event", mEvent);

        startActivity(intent);
        this.finish();
    }
}