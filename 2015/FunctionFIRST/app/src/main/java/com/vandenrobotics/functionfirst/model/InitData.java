package com.vandenrobotics.functionfirst.model;

import android.os.Parcel;
import android.os.Parcelable;

public class InitData implements Parcelable {
    public int teamNumber;
    public int matchNumber;
    public int allianceColor;
    public boolean noShow;

    public InitData(){
        teamNumber = 0;
        matchNumber = 0;
        allianceColor = 0;
        noShow = false;
    }

    public InitData(String string){
        this();
        try{
            String[] dataString = string.split(",");
            int[] data = new int[dataString.length];

            try{
                for(int i = 0; i < data.length; i++)
                    data[i] = Integer.parseInt(dataString[i]);
            } catch (NumberFormatException e){
                e.printStackTrace();
            }

            matchNumber = data[0];
            teamNumber = data[1];
            allianceColor = data[2];
            noShow = (data[3]==1);

        } catch (IndexOutOfBoundsException e){
            e.printStackTrace();
        }
    }

    public InitData(InitData initData){
        this();
        teamNumber = initData.teamNumber;
        matchNumber = initData.matchNumber;
        allianceColor = initData.allianceColor;
        noShow = initData.noShow;
    }

    @Override
    public String toString(){
        int tempNoShow = (noShow)? 1 : 0;
        return matchNumber+","+teamNumber+","+allianceColor+","+tempNoShow;
    }

    @Override
    public int describeContents() {
        // TODO Auto-generated method stub
        return 0;
    }

    @Override
    public void writeToParcel(Parcel arg0, int arg1) {
        // TODO Auto-generated method stub
        arg0.writeString(this.toString());
    }

    public static final Parcelable.Creator CREATOR = new Parcelable.Creator() {
        public InitData createFromParcel(Parcel in){
            return new InitData(in.readString());
        }

        public InitData[] newArray(int size){
            return new InitData[size];
        }
    };

}
