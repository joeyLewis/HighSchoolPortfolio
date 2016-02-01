package com.vandenrobotics.ragunasf.model;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Comparator;

/**
 * Created by Joe on 7/30/15.
 * contains information about a single match, including what level of competition,
 * the set_number, the match_number, and the alliances and teams on each alliance
 */
public class Match {

    public enum CompLevel{
        P,  // practice
        Q,  // qualifications
        QF, // quarter-finals
        SF, // semi-finals
        F;  // finals
    }

    // once a Match is initialized, you cannot change the CompLevel, set_number, or match_number
    // but you can update the teams participating based on your scouting position
    private final CompLevel comp_level;
    private final int set_number;
    private final int match_number;
    private ArrayList<Team> redAlliance;
    private ArrayList<Team> blueAlliance;

    /**
     * creates a Match object and assigns alliances, useful when the match is present on TheBlueAlliance
     * @param comp_level: the enum value defining what portion of competition the match is from (P, Q, QF, SF, or F)
     * @param set_number: the integer value defining what set of matches the match comes from (i.e. QF1, 2, 3, or 4)
     * @param match_number: the integer value defining which match number is being played (i.e. Q1, or F1, or SF1-2)
     * @param redAlliance: the ArrayList of Team objects defining the teams participating on the red alliance
     * @param blueAlliance: the ArrayList of Team objects defining the teams participating on the blue alliance
     */
    public Match(CompLevel comp_level, int set_number, int match_number, ArrayList<Team> redAlliance, ArrayList<Team> blueAlliance){
        this.comp_level = comp_level;
        this.set_number = set_number;
        this.match_number = match_number;
        this.redAlliance = redAlliance;
        this.blueAlliance = blueAlliance;
    }

    /**
     * creates a Match object without assigning it teams, useful when the matchlist cannot be downloaded from TheBlueAlliance
     * @param comp_level: the enum value defining what portion of competition the match is from (P, Q, QF, SF, or F)
     * @param set_number: the integer value defining what set of matches the match comes from (i.e. QF1, 2, 3, or 4)
     * @param match_number: the integer value defining which match number is being played (i.e. Q1, or F1, or SF1-2)
     */
    public Match(CompLevel comp_level, int set_number, int match_number){
        this.comp_level = comp_level;
        this.set_number = set_number;
        this.match_number = match_number;
        this.redAlliance = new ArrayList<>();
        this.blueAlliance = new ArrayList<>();
    }

    /**
     * creates a Match object from a string following the format of toString
     * @param s the string to create the Match object from
     */
    public Match(String s){
        CompLevel comp_level;
        int set_number, match_number;
        ArrayList<Team> redAlliance, blueAlliance;

        try {
            JSONObject details = new JSONObject(s);
            comp_level = (CompLevel)details.get("comp_level");
            set_number = details.getInt("set_number");
            match_number = details.getInt("match_number");
            redAlliance = (ArrayList<Team>)details.get("redAlliance");
            blueAlliance = (ArrayList<Team>)details.get("blueAlliance");
        } catch (JSONException e){
            e.printStackTrace();
            comp_level = CompLevel.Q;
            set_number = match_number = 1;
            redAlliance = blueAlliance = new ArrayList<>();
        }

        this.comp_level = comp_level;
        this.set_number = set_number;
        this.match_number = match_number;
        this.redAlliance = redAlliance;
        this.blueAlliance = blueAlliance;

    }

    /**
     * overridden method to turn the Match into a string for writing purposes
     * @return the string representing the details needed to later recreate the object
     */
    @Override
    public String toString(){
        JSONObject details = new JSONObject();
        try {
            details.put("comp_level", comp_level);
            details.put("set_number", set_number);
            details.put("match_number", match_number);
            details.put("red_alliance", redAlliance);
            details.put("blue_alliance", blueAlliance);
        } catch (JSONException e){
            e.printStackTrace();
        }

        return details.toString();
    }

    /**
     * method to turn the match into a sensible display for listing purposes
     * @return the String in the Format "CompLevelSetNumber-MatchNumber"
     */
    public String getListDetails(){
        return    comp_level.toString() +
                ((comp_level == CompLevel.QF || comp_level == CompLevel.SF)? String.valueOf(set_number) + "-" : "") +
                String.valueOf(match_number);
    }

    public CompLevel getCompLevel(){
        return comp_level;
    }

    public int getNumber(){
        return match_number;
    }

    public int getSetNumber(){
        return set_number;
    }

    public ArrayList<Team> getAlliance(AllianceCaptain allianceCaptain){
        switch(allianceCaptain){
            case Red:
                return redAlliance;
            case Blue:
                return blueAlliance;
            default:
                return null;
        }
    }

    public void setAlliance(AllianceCaptain allianceCaptain, ArrayList<Team> alliance){
        switch(allianceCaptain){
            case Red:
                this.redAlliance = alliance;
                break;
            case Blue:
                this.blueAlliance = alliance;
                break;
            default:
                break;
        }
    }

    public Team getTeam(ScoutingPosition scoutingPosition){
        switch(scoutingPosition) {
            case RedTeam1:
                try {
                    return redAlliance.get(0);
                } catch (IndexOutOfBoundsException e) {
                    e.printStackTrace();
                    return null;
                }
            case RedTeam2:
                try {
                    return redAlliance.get(1);
                } catch (IndexOutOfBoundsException e) {
                    e.printStackTrace();
                    return null;
                }
            case RedTeam3:
                try {
                    return redAlliance.get(2);
                } catch (IndexOutOfBoundsException e) {
                    e.printStackTrace();
                    return null;
                }
            case BlueTeam1:
                try {
                    return blueAlliance.get(0);
                } catch (IndexOutOfBoundsException e) {
                    e.printStackTrace();
                    return null;
                }
            case BlueTeam2:
                try {
                    return blueAlliance.get(1);
                } catch (IndexOutOfBoundsException e) {
                    e.printStackTrace();
                    return null;
                }
            case BlueTeam3:
                try {
                    return blueAlliance.get(2);
                } catch (IndexOutOfBoundsException e) {
                    e.printStackTrace();
                    return null;
                }
            default:
                return null;
        }
    }

    public void setTeam(ScoutingPosition scoutingPosition, Team team){
        switch(scoutingPosition){
            case RedTeam1:
                try{
                    redAlliance.set(0, team);
                } catch(IndexOutOfBoundsException e){
                    redAlliance.add(0, team);
                }
                break;
            case RedTeam2:
                try{
                    redAlliance.set(1, team);
                } catch(IndexOutOfBoundsException e){
                    redAlliance.add(1, team);
                }
                break;
            case RedTeam3:
                try{
                    redAlliance.set(2, team);
                } catch(IndexOutOfBoundsException e){
                    redAlliance.add(2, team);
                }
                break;
            case BlueTeam1:
                try{
                    blueAlliance.set(0, team);
                } catch(IndexOutOfBoundsException e){
                    blueAlliance.add(0, team);
                }
                break;
            case BlueTeam2:
                try{
                    blueAlliance.set(1, team);
                } catch(IndexOutOfBoundsException e){
                    blueAlliance.add(1, team);
                }
                break;
            case BlueTeam3:
                try{
                    blueAlliance.set(2, team);
                } catch(IndexOutOfBoundsException e){
                    blueAlliance.add(2, team);
                }
                break;
            default:
                break;
        }
    }

    public static class MatchComparator implements Comparator<Match> {
        @Override
        public int compare(Match a, Match b) {
            // sort Matches based on 3 levels of sorting structure - first by CompLevel, then by match_number, then finally by set_number
            int result = a.comp_level.compareTo(b.comp_level);
            int result2 = (result!=0)? result : Integer.compare(a.match_number, b.match_number);
            return (result2!=0) ? result2 : Integer.compare(a.set_number, b.set_number);
        }
    }

}

