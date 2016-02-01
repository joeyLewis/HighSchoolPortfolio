package com.vandenrobotics.functionfirst.scout.model;

/**
 * Created by Joey on 9/23/2014.
 */
public class MatchData{
    public InitData initData;
    public AutoData autoData;
    public TeleData teleData;
    public PostData postData;

    public MatchData(){
        initData = new InitData();
        autoData = new AutoData();
        teleData = new TeleData();
        postData = new PostData();
    }

    @Override
    public String toString(){
        return initData.toString()+"$"+autoData.toString()+"$"
                +teleData.toString()+"$"+postData.toString();
    }

    public boolean fromString(String string){
        String[] dataString = string.split("\\$");
        return (initData.fromString(dataString[0])&&autoData.fromString(dataString[1])
                &&teleData.fromString(dataString[2])&&postData.fromString(dataString[3]));
    }
}
