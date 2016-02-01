package com.vandenrobotics.functionfirst.model;

import android.os.Parcel;
import android.os.Parcelable;

public class AutoData implements Parcelable {

    public boolean hadAuto;

    public int totesToAuto;
    public int containersToAuto;
    public int containersFromStep;
    public int totesFromStep;

    public boolean[] autoStack;

    public boolean endInAuto;
    public boolean hadOther;


    public AutoData(){
        hadAuto = false;
        totesToAuto = 0;
        containersToAuto = 0;
        containersFromStep = 0;
        totesFromStep = 0;

        autoStack = new boolean[3];
        for(int i =0; i < autoStack.length; i++)
            autoStack[i] = false;

        endInAuto = false;
        hadOther = false;
    }

    public AutoData(String string){
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

            int index = 0;

            hadAuto = (data[index]==1);
            index += 1;
            totesToAuto = data[index];
            index += 1;
            containersToAuto = data[index];
            index += 1;
            containersFromStep = data[index];
            index += 1;
            totesFromStep = data[index];
            index += 1;

            for(int i = 0; i < autoStack.length; i++) {
                autoStack[i] = (data[index] == 1);
                index += 1;
            }

            endInAuto = (data[index]==1);
            index += 1;
            hadOther = (data[index]==1);

        } catch (IndexOutOfBoundsException e){
            e.printStackTrace();
        }
    }

    public AutoData(AutoData autoData){
        this();
        hadAuto = autoData.hadAuto;
        totesToAuto = autoData.totesToAuto;
        containersToAuto = autoData.containersToAuto;
        containersFromStep = autoData.containersFromStep;
        totesFromStep = autoData.totesFromStep;
        autoStack = new boolean[3];
        for(int i = 0; i < autoData.autoStack.length; i++){
            autoStack[i] = autoData.autoStack[i];
        }
        endInAuto = autoData.endInAuto;
        hadOther = autoData.hadOther;
    }

    @Override
    public String toString(){
        int tempAuto = hadAuto? 1 : 0;
        int tempStackBase = autoStack[0]? 1 : 0;
        int tempStackMid = autoStack[1]? 1 : 0;
        int tempStackTop = autoStack[2]? 1 : 0;
        int tempEndAuto = endInAuto? 1 : 0;
        int tempOther = hadOther? 1 : 0;

        return tempAuto+","+totesToAuto+","+containersToAuto+","+
                containersFromStep+","+totesFromStep+","+
                tempStackBase+","+tempStackMid+","+tempStackTop+","+
                tempEndAuto+","+tempOther;
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
        public AutoData createFromParcel(Parcel in){
            return new AutoData(in.readString());
        }

        public AutoData[] newArray(int size){
            return new AutoData[size];
        }
    };
}
