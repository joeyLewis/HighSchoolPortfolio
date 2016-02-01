package com.vandenrobotics.functionfirst.activities;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import com.vandenrobotics.functionfirst.R;

/**
 * MainActivity screen which handles the main menus that allow the
 * user to navigate through to the rest of the application
 * Includes --> Scout Activity for a certain event (as chosen by user)
 *          --> About Message
 */
public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void activityEventList(View view) {
        // open the EventListActivity
        Intent intent = new Intent(this, EventListActivity.class);
        startActivity(intent);
    }

    public void messageAbout(View view) {
        AlertDialog.Builder messageAbout = new AlertDialog.Builder(this);
        messageAbout.setTitle(R.string.text_titleAbout);
        messageAbout.setMessage(R.string.text_messageAbout)
            .setPositiveButton(R.string.button_ok, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    // pass through and simply close the dialog
                }
            })
            .show();
    }

}