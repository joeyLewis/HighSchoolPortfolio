package com.vandenrobotics.functionfirst.model;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.ArrayList;

/**
 * Created by Programming701-A on 1/31/2015.
 */
public class TeleData implements Parcelable {

    public ArrayList<Stack> stacks;         // all the stacks for the match
    public ArrayList<StepStack> stepStacks; // all of the stacks made on the step for the match (up to 3 that this robot can contribute to)

    public int totesFromChute;
    public int litterFromChute;
    public int totesFromLandfill;
    public int litterToLandfill;

    public TeleData(){
        stacks = new ArrayList<>();
        stepStacks = new ArrayList<>();
        totesFromChute = 0;
        litterFromChute = 0;
        totesFromLandfill = 0;
        litterToLandfill = 0;
    }

    public TeleData(String string){
        this();
        try{
            String[] dataString = string.split(",");
            float[] data = new float[dataString.length];

            for(int i = 0; i < data.length; i++){
                data[i]=Float.parseFloat(dataString[i]);
            }

            int index = 0;

            int numStacks = (int)data[index];
            index++;

            ArrayList<Stack> stk = new ArrayList<>();
            for(int i = 0; i < numStacks; i++){
                String stackString =
                        dataString[index   ]+","+dataString[index+1 ]+","+
                        dataString[index+2 ]+","+dataString[index+3 ]+","+
                        dataString[index+4 ]+","+dataString[index+5 ]+","+
                        dataString[index+6 ]+","+dataString[index+7 ]+","+
                        dataString[index+8 ]+","+dataString[index+9 ]+","+
                        dataString[index+10]+","+dataString[index+11];
                stk.add(new Stack(stackString));
                index+=12;
            }
            stacks = stk;

            int numStepStacks = (int)data[index];
            index++;

            ArrayList<StepStack> ststk = new ArrayList<>();
            for(int i = 0; i < numStepStacks; i++){
                String stepStackString =
                        dataString[index  ]+","+dataString[index+1]+","+
                        dataString[index+2]+","+dataString[index+3]+","+
                        dataString[index+4]+","+dataString[index+5]+","+
                        dataString[index+6]+","+dataString[index+7]+","+
                        dataString[index+8];
                ststk.add(new StepStack(stepStackString));
                index+=9;
            }
            stepStacks = ststk;

            totesFromChute = (int)data[index];

            index++;
            litterFromChute = (int)data[index];

            index++;
            totesFromLandfill = (int)data[index];

            index++;
            litterToLandfill = (int)data[index];


        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public TeleData(TeleData teleData) {
        this();

        stacks = teleData.stacks;
        stepStacks = teleData.stepStacks;
        totesFromChute = teleData.totesFromChute;
        litterFromChute = teleData.litterFromChute;
        totesFromLandfill = teleData.totesFromLandfill;
        litterToLandfill = teleData.litterToLandfill;
    }

    @Override
    public String toString(){
        int numStacks = stacks.size();
        int numStepStacks = stepStacks.size();

        String returnText = ""+numStacks+",";

        for(int i = 0; i < numStacks; i++){
            returnText+=stacks.get(i).toString();
            returnText+=",";
        }

        returnText+=numStepStacks;
        returnText+=",";

        for(int i = 0; i < numStepStacks; i++){
            returnText+=stepStacks.get(i).toString();
            returnText+=",";
        }

        String finalText = totesFromChute+","+litterFromChute+","+
                           totesFromLandfill+","+litterToLandfill;

        returnText+=finalText;

        return returnText;
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
        public TeleData createFromParcel(Parcel in){
            return new TeleData(in.readString());
        }

        public TeleData[] newArray(int size){
            return new TeleData[size];
        }
    };
}
