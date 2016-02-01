package com.vandenrobotics.functionfirst.model;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by Programming701-A on 2/10/2015.
 */
public class MatchData implements Parcelable{

    public InitData mInitData;
    public AutoData mAutoData;
    public TeleData mTeleData;
    public PostData mPostData;

    public MatchData(){
        mInitData = new InitData();
        mAutoData = new AutoData();
        mTeleData = new TeleData();
        mPostData = new PostData();
    }

    public MatchData(String string){
        this();
        try{
            String[] dataString = string.split("\\$");
            mInitData = new InitData(dataString[0]);
            mAutoData = new AutoData(dataString[1]);
            mTeleData = new TeleData(dataString[2]);
            mPostData = new PostData(dataString[3]);
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public MatchData(MatchData matchData){
        mInitData = matchData.mInitData;
        mAutoData = matchData.mAutoData;
        mTeleData = matchData.mTeleData;
        mPostData = matchData.mPostData;
    }

    @Override
    public String toString(){
        return mInitData.toString()+"$"+mAutoData.toString()+"$"+
               mTeleData.toString()+"$"+mPostData.toString();
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
        public MatchData createFromParcel(Parcel in){
            return new MatchData(in.readString());
        }

        public MatchData[] newArray(int size){
            return new MatchData[size];
        }
    };
}
