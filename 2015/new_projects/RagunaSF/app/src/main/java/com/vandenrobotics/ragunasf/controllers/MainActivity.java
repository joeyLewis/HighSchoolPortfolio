package com.vandenrobotics.ragunasf.controllers;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.ListView;

import com.loopj.android.http.JsonHttpResponseHandler;

import com.vandenrobotics.ragunasf.R;
import com.vandenrobotics.ragunasf.model.Event;
import com.vandenrobotics.ragunasf.tools.JSONTools;
import com.vandenrobotics.ragunasf.tools.MenuTools;
import com.vandenrobotics.ragunasf.tools.TheBlueAllianceRestClient;
import com.vandenrobotics.ragunasf.adapters.EventListAdapter;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;

/**
 * Created by Joe on 7/23/15.
 * handles the launcher screen of the application
 * allows searching for an event by name or location
 */
public class MainActivity extends Activity {

    // adapter for the EventList - handles filtering and sorting the list
    private EventListAdapter mAdapter;

    // the list of events found on TheBlueAlliance
    private ArrayList<Event> tbaEvents;

    // the list of events found locally on the device
    private ArrayList<Event> downloadedEvents;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // initialize tbaEvents to an empty ArrayList, to be populated later
        tbaEvents = new ArrayList<>();

        // initialize downloadedEvents to be read in from the locally saved file of events
        downloadedEvents = new ArrayList<>(); //ExternalStorageTools.readEvents();
        mAdapter = new EventListAdapter(this, downloadedEvents);

        if(downloadedEvents.isEmpty()){
            downloadEvents();
        }

        EditText EventsEditText = (EditText)findViewById(R.id.editText_Events);
        ListView EventList = (ListView)findViewById(R.id.listView_Events);

        EventList.setTextFilterEnabled(true);
        EventList.setAdapter(mAdapter);

        EventsEditText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                mAdapter.getFilter().filter(s);
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        // process a click on an item and pass the event into the new activity
        EventList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                startActivity(loadEvent(mAdapter.getItem(position)));
            }
        });

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        switch(item.getItemId()){
            case R.id.action_settings:
                break;
            case R.id.action_refreshEvents:
                // refresh and download new events
                downloadEvents();
                break;
            case R.id.action_loadWebsite:
                // load the website, asking for permission to navigate away from the app
                MenuTools.loadWebsite(getFragmentManager());
                break;
            case R.id.action_about:
                MenuTools.about(this);
                break;
            default:
                break;
        }

        return super.onOptionsItemSelected(item);
    }

    /**
     * attempts to access TheBlueAlliance and gather information from it on events and save them locally
     * if an event hasn't been downloaded before, it adds it to the list of local events for access without internet services
     * the user will still need internet to access the teams and matches of the event if they haven't done so before
     */
    private void downloadEvents(){

        // create a ProgressDialog to show downloading progress of events
        final ProgressDialog eventProgressDialog = ProgressDialog.show(
                this, getResources().getString(R.string.dialog_EventProgressTitle),
                      getResources().getString(R.string.dialog_EventProgressMessage));

        // check online status to see if we can load the Blue Alliance Data, otherwise load the list without it
        if (TheBlueAllianceRestClient.isOnline(this)) {
            TheBlueAllianceRestClient.get(this, "events/", new JsonHttpResponseHandler() {
                // no need to pass a year to the API, as it will default to the current year, which is always what we want
                @Override
                public void onSuccess(int statusCode, Header[] headers, JSONArray events) {
                    // handle the incoming JSONArray of events and populate the list view
                    try {
                        ArrayList<JSONObject> eventList = JSONTools.parseJSONArray(events);
                        for(JSONObject jso : eventList){
                            tbaEvents.add(new Event(jso.getString("key"),jso.getString("name"),jso.getString("short_name"),jso.getString("location")));
                        }

                        boolean eventAlreadyDownloaded = false;
                        for(Event event : tbaEvents){
                            eventProgressDialog.setMessage("Checking Event: " + event.getKey());

                            for(Event localEvent : downloadedEvents){
                                if(event.getKey().equals(localEvent.getKey())){
                                    eventAlreadyDownloaded=true;
                                    break;
                                }
                            }

                            if(!eventAlreadyDownloaded){
                                eventProgressDialog.setMessage("Downloading New Event: " + event.getKey());
                                downloadedEvents.add(event);
                            }

                            eventAlreadyDownloaded = false;
                        }

                        // sort the final array and tell the adapter to update just in case
                        Collections.sort(downloadedEvents, new Event.EventComparator());
                        mAdapter.notifyDataSetChanged();

                        eventProgressDialog.setMessage("Successfully accessed remote host - www.thebluealliance.com");

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    eventProgressDialog.dismiss();
                }

                @Override
                public void onFailure(int statusCode, Header[] headers, Throwable t, JSONObject jo) {
                    eventProgressDialog.dismiss();
                }
            });

        } else {
            eventProgressDialog.setMessage("You aren't connected to the internet.  Proceeding with current local list of events...");
            eventProgressDialog.dismiss();
        }
    }

    /**
     * processes a JSONObject representing an event and returns an Intent setup to load that event into the EventActivity
     * @param event: the event to load into the EventActivity
     * @return: an Intent designed to send the JSONObject event as a string to be retrieved later by the EventActivity
     */
    private Intent loadEvent(Event event){
        return new Intent(this, EventActivity.class).putExtra("event", event.toString());
    }

}
