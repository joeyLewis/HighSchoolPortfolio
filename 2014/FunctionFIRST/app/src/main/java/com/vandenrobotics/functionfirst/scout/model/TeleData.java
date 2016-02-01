package com.vandenrobotics.functionfirst.scout.model;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.ArrayList;

/**
 * Created by Joey on 9/23/2014.
 */
public class TeleData implements Parcelable{
    public ArrayList<Double> intakeTimes;
    public int lowScore;
    public ArrayList<HotSpot> hotSpots;

    public TeleData(){
        intakeTimes = new ArrayList<Double>();
        lowScore = 0;
        hotSpots = new ArrayList<HotSpot>();
    }

    @Override
    public String toString(){
        int numIntakes = intakeTimes.size();
        int numHotSpots = hotSpots.size();

        String returnValue = ""+numIntakes+",";
        for(int i = 0; i < numIntakes; i++){
            returnValue += intakeTimes.get(i);
            returnValue += ",";
        }

        returnValue+=lowScore;
        returnValue+=",";

        returnValue+=numHotSpots;
        returnValue+=",";
        for(int i = 0; i < numHotSpots; i++){
            returnValue += hotSpots.get(i).type;
            returnValue += ",";
            returnValue += hotSpots.get(i).x;
            returnValue += ",";
            returnValue += hotSpots.get(i).y;
            returnValue += ",";
        }
        returnValue = returnValue.substring(0,returnValue.lastIndexOf(","));

        return returnValue;
    }

    public boolean fromString(String string){
        try{
            System.out.println("TELEDATA: " + string);
            String[] dataString = string.split(",");
            double[] data = new double[dataString.length];

            try{
                for(int i = 0; i < data.length; i++)
                    data[i] = Double.parseDouble(dataString[i]);
            } catch (NumberFormatException e){
                e.printStackTrace();
                return false;
            } catch (IndexOutOfBoundsException e){
                e.printStackTrace();
                return false;
            }

            int index = 0;
            int numIntakes = (int)data[index];
            index += 1;
            ArrayList<Double> intakes = new ArrayList<Double>();
            for(int i = 0; i < numIntakes; i++){
                intakes.add(data[index]);
                index+=1;
            }
            intakeTimes = intakes;

            lowScore = (int)data[index];
            index += 1;

            int numHotSpots = (int)data[index];
            index += 1;
            ArrayList<HotSpot> hSpots = new ArrayList<HotSpot>();

            for(int i = 0; i < numHotSpots; i++){
                HotSpot hotSpot = new HotSpot((int)data[index],data[index+1],data[index+2]);
                index+=3;
                hSpots.add(hotSpot);
            }
            hotSpots = hSpots;


        } catch (IndexOutOfBoundsException e){
            e.printStackTrace();
            return false;
        } catch (Exception e){
            e.printStackTrace();
            return false;
        }
        // only way it can get to this point is if there are no exceptions
        return true;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {

    }
}
