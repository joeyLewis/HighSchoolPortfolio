package com.vandenrobotics.functionfirst.activities;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import com.loopj.android.http.JsonHttpResponseHandler;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.tools.ExternalStorageTools;
import com.vandenrobotics.functionfirst.tools.JSONTools;
import com.vandenrobotics.functionfirst.tools.TheBlueAllianceRestClient;
import com.vandenrobotics.functionfirst.views.EventArrayAdapter;
import com.vandenrobotics.functionfirst.views.EventListView;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class EventListActivity extends Activity {

    private ArrayList<JSONObject> tbaEvents = new ArrayList<>();
    private ArrayList<JSONObject> downloadedEvents = new ArrayList<>();

    private EventListView tbaListView;
    private EventArrayAdapter tbaAdapter;

    private ListView downloadedListView;
    private ArrayAdapter<JSONObject> downloadedAdapter;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_event_list);

        // create a progress dialog to make a visual representation of the downloads and reading files
        final ProgressDialog progressDialog = ProgressDialog.show(this, getResources().getString(R.string.text_titleProgress), getResources().getString(R.string.text_messageProgressEventList));
        progressDialog.setCancelable(true);

        // reset all Blue Alliance Events so that the list does not appear when we do not have internet connection
        tbaEvents = new ArrayList<>();

        // access all downloaded events and the corresponding json documents, putting them into an ArrayList
        downloadedEvents = ExternalStorageTools.readEvents();
        // sort the loaded list by start_date, then by name alphabetically
        downloadedEvents = JSONTools.sortJSONArray(downloadedEvents, "start_date", "name");

        // check online status to see if we can load the Blue Alliance Data, otherwise load the dialog without it
        if (TheBlueAllianceRestClient.isOnline(EventListActivity.this)) {
            TheBlueAllianceRestClient.get(EventListActivity.this, "events/", new JsonHttpResponseHandler() {
                // no need to pass a year to the API, as it will default to the current year, which is always what we want
                @Override
                public void onSuccess(int statusCode, Header[] headers, JSONArray events) {
                    // handle the incoming JSONArray of events and populate the list view
                    try {
                        tbaEvents = JSONTools.parseJSONArray(events);
                        tbaEvents = JSONTools.sortJSONArray(tbaEvents, "start_date", "name");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    loadEventList();
                    progressDialog.dismiss();
                }
                @Override
                public void onFailure(int statusCode, Header[] headers, Throwable t, JSONObject jo){
                    progressDialog.dismiss();
                    // create an alert dialog to let the user know that the request failed, and load the event lists for what events we do have downloaded
                    loadEventList();
                }
            });
        } else {
            loadEventList();
            progressDialog.dismiss();
        }

    }

    private void loadEventList() {

        tbaListView = (EventListView) findViewById(R.id.tbaEventListView);
        tbaAdapter = new EventArrayAdapter(tbaEvents, this);
        tbaListView.setAdapter(tbaAdapter);

        downloadedListView = (ListView) findViewById(R.id.downloadEventListView);
        downloadedAdapter = new ArrayAdapter<JSONObject>(this, android.R.layout.simple_list_item_2, android.R.id.text1, downloadedEvents){
            @Override
            public View getView(int position, View convertView, ViewGroup parent) {
                View view = super.getView(position, convertView, parent);
                TextView text1 = (TextView) view.findViewById(android.R.id.text1);
                TextView text2 = (TextView) view.findViewById(android.R.id.text2);

                try {
                    text1.setText(downloadedEvents.get(position).getString("name"));
                    text2.setText("Start Date: " + downloadedEvents.get(position).getString("start_date"));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                return view;
            }
        };
        downloadedListView.setAdapter(downloadedAdapter);

        // download event for later feature
        tbaListView.setOnItemClickListener(new ListView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapter, View v, int position, long arg3) {
                JSONObject event = (JSONObject) adapter.getItemAtPosition(position);

                // perform TheBlueAllianceRestClient get on that value, and run the saving of data and pictures, etc. to a competition file
                downloadNewEvent(event);
            }
        });

        // download event for later feature
        tbaListView.setOnItemLongClickListener(new ListView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> adapter, View v, final int position, long arg3) {
                JSONObject event = (JSONObject) adapter.getItemAtPosition(position);

                // download the event but do not load it immediately (downloading for later)
                downloadNewEvent(event);
                return true; // do not also run the regular click event
            }
        });

        // load downloaded event feature
        downloadedListView.setOnItemClickListener(new ListView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapter, View v, int position, long arg3) {
                JSONObject event = (JSONObject) adapter.getItemAtPosition(position);

                // send the event key to the ScoutActivity to gather all data in that directory
                startActivity(loadEventToScout(event));
            }
        });

        // delete downloaded event feature
        downloadedListView.setOnItemLongClickListener(new ListView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> adapter, View v, final int position, long arg3) {
            AlertDialog.Builder messageConfirmDelete = new AlertDialog.Builder(EventListActivity.this);
            messageConfirmDelete.setTitle(R.string.text_titleConfirmDelete);
            messageConfirmDelete.setMessage(R.string.text_messageConfirmDelete)
                .setPositiveButton(R.string.button_ok, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // delete the event and all relative data
                        try {
                            ExternalStorageTools.deleteFiles(downloadedEvents.get(position).getString("key"));
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        downloadedEvents.remove(position);
                        downloadedEvents = JSONTools.sortJSONArray(downloadedEvents, "start_date", "name");
                        downloadedAdapter.notifyDataSetChanged();

                        ExternalStorageTools.writeEvents(downloadedEvents);
                    }
                })
                .setNegativeButton(R.string.button_cancel, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // pass through and close the dialog
                    }
                })
                .show();
            return true; // do not also run the regular click event
            }
        });
    }

    private void downloadNewEvent(final JSONObject event){

        // add event to the list of downloaded events if it is new, then proceed to grab all downloadable information about it
        // if the event is not new, create a dialog alerting the user that the event has already been downloaded.

        // create a dialog to show user that the activity is working
        final ProgressDialog progressDialog = ProgressDialog.show(this, getResources().getString(R.string.text_titleProgress), getResources().getString(R.string.text_messageProgressDownload));
        progressDialog.setCancelable(true);

        boolean newEvent = true;

        // check to make sure the event is new
        try {
            for (int i = 0; i < downloadedEvents.size(); i++) {
                if (downloadedEvents.get(i).getString("name").equals(event.getString("name"))) {
                    newEvent = false;
                    break;
                }
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

        if (newEvent) {
            if(TheBlueAllianceRestClient.isOnline(EventListActivity.this)) {
                try {
                    TheBlueAllianceRestClient.get(EventListActivity.this, "event/" + event.getString("key") + "/teams", new JsonHttpResponseHandler() {
                        @Override
                        public void onSuccess(int statusCode, Header[] headers, JSONArray teams) {
                            // handle the incoming JSONArray of teams and write them to a file
                            try {
                                final ArrayList<JSONObject> teamlist = JSONTools.sortJSONArray(JSONTools.parseJSONArray(teams), "team_number");
                                ExternalStorageTools.writeTeams(teamlist, event.getString("key"));

                                downloadedEvents.add(event);
                                downloadedEvents = JSONTools.sortJSONArray(downloadedEvents, "start_date", "name");
                                downloadedAdapter.notifyDataSetChanged();

                                ExternalStorageTools.writeEvents(downloadedEvents);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            progressDialog.dismiss();
                        }
                    });

                } catch (JSONException e) {
                    e.printStackTrace();
                    progressDialog.dismiss();
                }
            } else {
                progressDialog.dismiss();
                AlertDialog.Builder messageAlreadyDownloaded = new AlertDialog.Builder(EventListActivity.this);
                messageAlreadyDownloaded.setTitle(R.string.text_titleNoInternet);
                messageAlreadyDownloaded.setMessage(R.string.text_messageNoInternet)
                        .setPositiveButton(R.string.button_ok, new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int id) {
                                // pass through and close the dialog
                            }
                        })
                        .show();
            }
        } else {
            progressDialog.dismiss();
            AlertDialog.Builder messageAlreadyDownloaded = new AlertDialog.Builder(EventListActivity.this);
            messageAlreadyDownloaded.setTitle(R.string.text_titleAlreadyDownloaded);
            messageAlreadyDownloaded.setMessage(R.string.text_messageAlreadyDownloaded)
                    .setPositiveButton(R.string.button_ok, new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {
                            // pass through and close the dialog
                        }
                    })
                    .show();
        }
    }

    private Intent loadEventToScout(JSONObject event){
        Intent intent = new Intent(this, ScoutActivity.class);
        try {
            intent.putExtra("event", event.getString("key"));
        } catch (JSONException e){
            e.printStackTrace();
        }
        return intent;
    }
}
