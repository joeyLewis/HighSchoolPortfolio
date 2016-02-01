package com.vandenrobotics.functionfirst;

import android.os.Bundle;

import android.app.Activity;
import android.app.AlertDialog;

import android.view.View;

import android.content.Intent;
import android.widget.TextView;

import com.vandenrobotics.functionfirst.scout.ScoutActivity;


public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void goTo_scoutActivity(View view)
    {
        startActivity(new Intent(this,ScoutActivity.class));
    }

    public void showAbout(View view)
    {
        AlertDialog alert = new AlertDialog.Builder(this)
                .setTitle("FUNCTION FIRST " + getResources().getString(R.string.info_version))
                .setMessage("FUNCTION FIRST is an electronic scouting system for the FIRST Robotics Competition. \n" +
                            "Coded and Designed by: \n \t\t Joseph Lewis - FIRST Team 701")
                .show();
        TextView msgText = (TextView) alert.findViewById(android.R.id.message);
        msgText.setTextSize((float) 16.0);
    }

}
