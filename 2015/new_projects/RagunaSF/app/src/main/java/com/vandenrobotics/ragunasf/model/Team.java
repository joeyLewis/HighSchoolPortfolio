package com.vandenrobotics.ragunasf.model;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Comparator;

/**
 * Created by Joe on 7/30/15.
 * contains all relevant information about a team, including their number and nickname
 */
public class Team {

    private final int number;
    private final String nickname;

    public Team(int number, String nickname){
        this.number = number;
        this.nickname = nickname;
    }

    public Team(String s){
        int number;
        String nickname;

        try {
            JSONObject details = new JSONObject(s);
            number = details.getInt("number");
            nickname = details.getString("nickname");
        } catch (JSONException e){
            e.printStackTrace();
            number = 0;
            nickname = null;
        }

        this.number = number;
        this.nickname = nickname;
    }

    @Override
    public String toString(){
        JSONObject details = new JSONObject();
        try{
            details.put("number", number);
            details.put("nickname", nickname);
        } catch (JSONException e){
            e.printStackTrace();
        }

        return details.toString();
    }

    public int getNumber(){
        return number;
    }

    public String getNickname(){
        return nickname;
    }

    public static class TeamComparator implements Comparator<Team> {
        @Override
        public int compare(Team a, Team b){
            //sort teams solely based on their number, smallest to largest
            return Integer.compare(a.number, b.number);
        }
    }
}
