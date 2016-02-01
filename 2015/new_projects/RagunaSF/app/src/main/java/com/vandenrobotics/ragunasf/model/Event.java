package com.vandenrobotics.ragunasf.model;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Comparator;

/**
 * Created by Joe on 7/31/15.
 * Event class handles all the information we need to know about an event
 * once the JSONDocuments are gathered from the blue alliance, we parse data down to just this information
 * because we do not need all of the other information about an event
 */
public class Event {

    private final String key;
    private final String name;
    private final String short_name;
    private final String location;

    private ArrayList<Match> matches;
    private ArrayList<Team> teams;

    public Event(String key, String name, String short_name, String location){
        this.key = key;
        this.name = name;
        this.short_name = short_name;
        this.location = location;
    }

    public Event(String s){
        String key, name, short_name, location;

        try {
            JSONObject details = new JSONObject(s);
            key = details.getString("key");
            name = details.getString("name");
            short_name = details.getString("short_name");
            location = details.getString("location");
        } catch (JSONException e){
            e.printStackTrace();
            key = null;
            name = null;
            short_name = null;
            location = null;
        }

        this.key = key;
        this.name = name;
        this.short_name = short_name;
        this.location = location;
    }

    @Override
    public String toString(){
        JSONObject details = new JSONObject();
        try {
            details.put("key", key);
            details.put("name", name);
            details.put("short_name", short_name);
            details.put("location", location);
        } catch (JSONException e){
            e.printStackTrace();
        }

        return details.toString();
    }

    public String getKey(){
        return key;
    }

    public String getName(){
        return name;
    }

    public String getShortName(){
        return short_name;
    }

    public String getLocation(){
        return location;
    }

    public String getTitle(){
        return short_name.equals("null")? name : short_name;
    }

    public void setMatches(ArrayList<Match> matches){
        this.matches = matches;
    }

    public ArrayList<Match> getMatches(){
        return matches;
    }

    public void setTeams(ArrayList<Team> teams){
        this.teams = teams;
    }

    public ArrayList<Team> getTeams(){
        return teams;
    }

    public static class EventComparator implements Comparator<Event> {
        @Override
        public int compare(Event a, Event b){
            //sort events based on their name only
            //TODO: add full functionality to short all events by start_date, into categories by week of competition, then by name
            return a.name.compareTo(b.name);
        }
    }
}
