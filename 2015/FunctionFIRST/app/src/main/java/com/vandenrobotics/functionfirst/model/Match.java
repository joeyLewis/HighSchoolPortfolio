package com.vandenrobotics.functionfirst.model;

/**
 * Created by Joey on 2/8/2015.
 */
public class Match {
    public int number;
    public int[] teams;

    public Match(){
        number = 0;
        teams = new int[6];
    }

    public Match(String s){
        try {
            String[] info = s.split(",");
            number = Integer.parseInt(info[0]);
            teams[0] = Integer.parseInt(info[1]);
            teams[1] = Integer.parseInt(info[2]);
            teams[2] = Integer.parseInt(info[3]);
            teams[3] = Integer.parseInt(info[4]);
            teams[4] = Integer.parseInt(info[5]);
            teams[5] = Integer.parseInt(info[6]);
        } catch (IndexOutOfBoundsException e){
            e.printStackTrace();
            number = 0;
            teams = new int[6];
        } catch (NumberFormatException e){
            e.printStackTrace();
            number = 0;
            teams = new int[6];
        }
    }

    public String toString(){
        return number + ","
                + teams[0] + ","
                + teams[1] + ","
                + teams[2] + ","
                + teams[3] + ","
                + teams[4] + ","
                + teams[5] + "\n";
    }
}
