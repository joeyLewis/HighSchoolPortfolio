package com.vandenrobotics.functionfirst.model;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by Programming701-A on 1/31/2015.
 */
public class PostData implements Parcelable {

    public int numFouls;
    public boolean gotRedCard;
    public boolean gotYellowCard;
    public boolean wasDisabled;

    public PostData(){
        numFouls = 0;
        gotRedCard = false;
        gotYellowCard = false;
        wasDisabled = false;
    }

    public PostData(String string){
        this();
        try{
            String[] dataString = string.split(",");
            int[] data = new int[dataString.length];

            try{
                for(int i = 0; i < data.length; i++)
                    data[i] = Integer.parseInt(dataString[i]);
            } catch (NumberFormatException e){
                e.printStackTrace();
            } catch (IndexOutOfBoundsException e){
                e.printStackTrace();
            }

            numFouls = data[0];
            gotRedCard = (data[1]==1);
            gotYellowCard = (data[2]==1);
            wasDisabled = (data[3]==1);

        } catch (IndexOutOfBoundsException e){
            e.printStackTrace();
        }
    }

    public PostData(PostData postData) {
        this();
        numFouls = postData.numFouls;
        gotRedCard = postData.gotRedCard;
        gotYellowCard = postData.gotYellowCard;
        wasDisabled = postData.wasDisabled;
    }

    @Override
    public String toString(){
        int tempRedCard = gotRedCard? 1 : 0;
        int tempYellowCard = gotYellowCard? 1 : 0;
        int tempDisabled = wasDisabled? 1 : 0;

        return numFouls+","+tempRedCard+","+tempYellowCard+","+tempDisabled;
    }

    @Override
    public int describeContents() {
        // TODO auto-generated method stub
        return 0;
    }

    @Override
    public void writeToParcel(Parcel arg0, int arg1) {
        // TODO auto-generated method stub
        arg0.writeString(this.toString());
    }

    public static final Parcelable.Creator CREATOR = new Parcelable.Creator() {
        public PostData createFromParcel(Parcel in){
            return new PostData(in.readString());
        }

        public PostData[] newArray(int size){
            return new PostData[size];
        }
    };
}
