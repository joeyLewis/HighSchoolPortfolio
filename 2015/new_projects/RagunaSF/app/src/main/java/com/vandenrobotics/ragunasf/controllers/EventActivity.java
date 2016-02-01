package com.vandenrobotics.ragunasf.controllers;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.support.v4.app.FragmentTabHost;

import com.loopj.android.http.JsonHttpResponseHandler;
import com.vandenrobotics.ragunasf.R;
import com.vandenrobotics.ragunasf.controllers.match.MatchSetupFragment;
import com.vandenrobotics.ragunasf.controllers.pits.PitSetupFragment;
import com.vandenrobotics.ragunasf.model.Event;
import com.vandenrobotics.ragunasf.model.Match;
import com.vandenrobotics.ragunasf.model.Team;
import com.vandenrobotics.ragunasf.tools.JSONTools;
import com.vandenrobotics.ragunasf.tools.MenuTools;
import com.vandenrobotics.ragunasf.tools.TheBlueAllianceRestClient;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;

public class EventActivity extends FragmentActivity {

    private Event mEvent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_event);

        // set the title of the EventActivity based on the String defining the event
        mEvent = new Event(getIntent().getStringExtra("event"));

        // load the teams attending this event based on locally saved data
        //mEvent.setTeams(ExternalStorageTools.readTeams(mEvent));

        // load the matches at this event based on locally saved data
        //mEvent.setMatches(ExternalStorageTools.readMatches(mEvent));

        setTitle(mEvent.getTitle());

        if(mEvent.getTeams()==null)
        {
            mEvent.setTeams(new ArrayList<Team>());
            // add a filler to the display in case the download fails
            mEvent.getTeams().add(new Team(0, "FILLER TEAM"));
            downloadTeams();
        }
        if(mEvent.getMatches()==null)
        {
            mEvent.setMatches(new ArrayList<Match>());
            // add a filler to the display in case the download fails
            mEvent.getMatches().add(new Match(Match.CompLevel.Q, 1, 0));
            downloadMatches();
        }

        //create the tabs for the different event options

        FragmentTabHost mTabHost = (FragmentTabHost)findViewById(R.id.tabHost_Setup);
        mTabHost.setup(this, getSupportFragmentManager(), android.R.id.tabcontent);

        mTabHost.addTab(mTabHost.newTabSpec("tab_pitSetup")
                .setIndicator(getResources().getString(R.string.tab_PitSetupTitle), null), PitSetupFragment.class, null);
        mTabHost.addTab(mTabHost.newTabSpec("tab_matchSetup")
                .setIndicator(getResources().getString(R.string.tab_MatchSetupTitle), null), MatchSetupFragment.class, null);

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_event, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        switch(item.getItemId()){
            case R.id.action_refreshEvent:
                downloadTeams();
                downloadMatches();
                break;
            case R.id.action_about:
                MenuTools.about(this);
            case R.id.action_loadWebsite:
                MenuTools.loadWebsite(getFragmentManager());
                break;
            case R.id.action_settings:
                break;
        }

        return super.onOptionsItemSelected(item);
    }

    /**
     * downloads the list of teams attending an event, if it is available
     */
    private void downloadTeams() {
        // create a ProgressDialog to show downloading progress of teams
        final ProgressDialog downloadTeamsProgressDialog = ProgressDialog.show(
                this, getResources().getString(R.string.dialog_DownloadTeamsProgressTitle),
                getResources().getString(R.string.dialog_DownloadTeamsProgressMessage));

        TheBlueAllianceRestClient.get(this, "event/" + mEvent.getKey() + "/teams", new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONArray incoming) {
                // handle the incoming JSONArray of teams and write them to a file
                try {
                    // saves the incoming list as a sorted array of JSONObjects based on the key "team_number"
                    ArrayList<JSONObject> teamlist = JSONTools.parseJSONArray(incoming);
                    ArrayList<Team> teams = new ArrayList<>();
                    for (JSONObject downloadedTeam : teamlist) {
                        teams.add(new Team(downloadedTeam.getInt("team_number"), downloadedTeam.getString("nickname")));
                    }
                    Collections.sort(teams, new Team.TeamComparator());
                    mEvent.setTeams(teams);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                downloadTeamsProgressDialog.dismiss();
            }
        });
    }

    /**
     * downloads the matchlist if it is available
     */
    private void downloadMatches(){
        // create a ProgressDialog to show downloading progress of matches
        final ProgressDialog downloadMatchesProgressDialog = ProgressDialog.show(
                this, getResources().getString(R.string.dialog_DownloadMatchesProgressTitle),
                getResources().getString(R.string.dialog_DownloadMatchesProgressMessage));

        TheBlueAllianceRestClient.get(this, "event/" + mEvent.getKey() + "/matches", new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONArray incoming) {
                // handle the incoming JSONArray of matches and write them to a file
                downloadMatchesProgressDialog.setMessage("Downloading Matches");
                try {
                    // saves the incoming list as a sorted array of JSONObjects based on the keys "comp_level" and "match_number"
                    ArrayList<JSONObject> matchlist = JSONTools.parseJSONArray(incoming);
                    ArrayList<Match> matches = new ArrayList<>();
                    for (JSONObject downloadedMatch : matchlist) {
                        Match.CompLevel compLevel;
                        switch (downloadedMatch.getString("comp_level").toUpperCase()) {
                            case "P":
                                compLevel = Match.CompLevel.P;
                                break;
                            case "Q":
                                compLevel = Match.CompLevel.Q;
                                break;
                            case "QF":
                                compLevel = Match.CompLevel.QF;
                                break;
                            case "SF":
                                compLevel = Match.CompLevel.SF;
                                break;
                            case "F":
                                compLevel = Match.CompLevel.F;
                                break;
                            default:
                                compLevel = Match.CompLevel.Q;
                                break;
                        }
                        JSONArray redTeams = downloadedMatch.getJSONObject("alliances").getJSONObject("red").getJSONArray("teams");
                        JSONArray blueTeams = downloadedMatch.getJSONObject("alliances").getJSONObject("blue").getJSONArray("teams");

                        ArrayList<Team> redAlliance = new ArrayList<>(3);
                        ArrayList<Team> blueAlliance = new ArrayList<>(3);
                        for(int i = 0; i < 3; i++){
                            redAlliance.add(i, getTeamFromNumber(Integer.valueOf(redTeams.getString(i).substring(3))));
                            blueAlliance.add(i, getTeamFromNumber(Integer.valueOf(blueTeams.getString(i).substring(3))));
                        }
                        matches.add(new Match(compLevel, downloadedMatch.getInt("set_number"), downloadedMatch.getInt("match_number"), redAlliance, blueAlliance));
                    }
                    Collections.sort(matches, new Match.MatchComparator());
                    mEvent.setMatches(matches);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                downloadMatchesProgressDialog.dismiss();
            }
        });
    }

    public Event getEvent(){
        return mEvent;
    }

    /**
     * finds a team among the list based off of its number
     * @param number the number with which to search for a team
     * @return the team which matches the number provided, or null if there is none
     */
    public Team getTeamFromNumber(int number){
        for(Team t : mEvent.getTeams()){
            if(number == t.getNumber()){
                return t;
            }
        }
        return null;
    }

}
