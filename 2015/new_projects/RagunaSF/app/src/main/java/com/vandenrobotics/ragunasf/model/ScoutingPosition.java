package com.vandenrobotics.ragunasf.model;

/**
 * Created by Joe on 7/30/15.
 * enum containing values and descriptions of the 6 possible regular scouting positions for match scouting
 */
public enum ScoutingPosition {
    RedTeam1 ("Red 1"),             // position for scouting red team 1
    RedTeam2 ("Red 2"),             // position for scouting red team 2
    RedTeam3 ("Red 3"),             // position for scouting red team 3
    BlueTeam1 ("Blue 1"),           // position for scouting blue team 1
    BlueTeam2 ("Blue 2"),           // position for scouting blue team 2
    BlueTeam3 ("Blue 3");           // position for scouting blue team 3

    private final String description;

    ScoutingPosition(String description){
        this.description = description;
    }

    @Override
    public String toString(){
        return description;
    }

}
