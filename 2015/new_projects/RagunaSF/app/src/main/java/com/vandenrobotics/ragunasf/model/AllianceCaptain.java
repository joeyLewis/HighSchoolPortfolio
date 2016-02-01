package com.vandenrobotics.ragunasf.model;

/**
 * Created by Joe on 7/31/15.
 */
public enum AllianceCaptain {
    Red ("Red Alliance"),   // red alliance captain position
    Blue ("Blue Alliance"); // blue alliance captain position

    private final String description;

    AllianceCaptain(String description){
        this.description = description;
    }

    @Override
    public String toString(){
        return description;
    }
}
