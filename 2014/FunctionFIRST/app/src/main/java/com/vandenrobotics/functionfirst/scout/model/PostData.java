package com.vandenrobotics.functionfirst.scout.model;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by Joey on 9/23/2014.
 */
public class PostData implements Parcelable{
    public int regFouls;
    public int techFouls;

    public boolean disabled;
    public boolean noShow;
    public boolean yellowCard;
    public boolean redCard;
    public boolean defensive;
    public boolean aggressive;

    public PostData(){
        regFouls = 0;
        techFouls = 0;

        disabled = false;
        noShow = false;
        yellowCard = false;
        redCard = false;
        defensive = false;
        aggressive = false;
    }

    @Override
    public String toString(){
        int tempDis = disabled? 1 : 0;
        int tempNoS = noShow? 1 : 0;
        int tempYel = yellowCard? 1 : 0;
        int tempRed = redCard? 1 : 0;
        int tempDef = defensive? 1 : 0;
        int tempAgg = aggressive? 1 : 0;

        return regFouls+","+techFouls+","
                +tempDis +","+tempNoS  +","
                +tempYel +","+tempRed  +","
                +tempDef +","+tempAgg;
    }

    public boolean fromString(String string){
        try{
            System.out.println("POSTDATA: " + string);
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

            regFouls = data[0];
            techFouls = data[1];
            disabled = (data[2]==1);
            noShow = (data[3]==1);
            yellowCard = (data[4]==1);
            redCard = (data[5]==1);
            defensive = (data[6]==1);
            aggressive = (data[7]==1);

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
