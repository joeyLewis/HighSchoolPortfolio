package com.vandenrobotics.functionfirst.scout.model;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by Joey on 9/23/2014.
 */
public class AutoData implements Parcelable {
    public boolean hadAuto;
    public boolean mobilityBonus;
    public boolean goalieZone;
    public boolean[] highHot = new boolean[3];
    public boolean[] lowHot = new boolean[3];

    public int highScore;
    public int lowScore;

    public AutoData(){
        hadAuto = false;
        mobilityBonus = false;
        goalieZone = false;
        highHot[0] = highHot[1] = highHot[2] = false;
        lowHot[0] = lowHot[1] = lowHot[2] = false;

        highScore = lowScore = 0;
    }

    @Override
    public String toString(){
        int tempAuto = hadAuto? 1 : 0;
        int tempMobil = mobilityBonus? 1 : 0;
        int tempGoalie = goalieZone? 1 : 0;
        int[] tempHH = new int[3];
        tempHH[0] = highHot[0]? 1 : 0;
        tempHH[1] = highHot[1]? 1 : 0;
        tempHH[2] = highHot[2]? 1 : 0;
        int[] tempLH = new int[3];
        tempLH[0] = lowHot[0]? 1 : 0;
        tempLH[1] = lowHot[1]? 1 : 0;
        tempLH[2] = lowHot[2]? 1 : 0;

        return tempAuto+","+tempMobil+","+tempGoalie+","+
                highScore+","+tempHH[0]+","+tempHH[1]+","+tempHH[2]+","+
                lowScore+","+tempLH[0]+","+tempLH[1]+","+tempLH[2];
    }

    public boolean fromString(String string){
        try{
            System.out.println("AUTODATA: " + string);
            String[] dataString = string.split(",");

            int[] data = new int[dataString.length];

            try{
                for(int i = 0; i < data.length; i++)
                    data[i] = Integer.parseInt(dataString[i]);
            } catch (NumberFormatException e){
                e.printStackTrace();
                return false;
            } catch (IndexOutOfBoundsException e){
                e.printStackTrace();
                return false;
            }

            hadAuto = (data[0]==1);
            mobilityBonus = (data[1]==1);
            goalieZone = (data[2]==1);
            highScore = data[3];
            highHot[0] = (data[4]==1);
            highHot[1] = (data[5]==1);
            highHot[2] = (data[6]==1);
            lowScore = data[7];
            lowHot[0] = (data[8]==1);
            lowHot[1] = (data[9]==1);
            lowHot[2] = (data[10]==1);

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
