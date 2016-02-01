package com.vandenrobotics.functionfirst.scout.model;

/**
 * Created by Joey on 9/23/2014.
 */
public class InitData{
    public int teamNumber;
    public int matchNumber;
    public int allianceColor;

    public InitData(){
        teamNumber = 0;
        matchNumber = 0;
        allianceColor = 0;
    }

    @Override
    public String toString(){
        return matchNumber + "," + teamNumber + "," + allianceColor;
    }

    public boolean fromString(String string){
        try{
            System.out.println("INITDATA: " + string);
            String[] dataString = string.split(",");
            int data[] = new int[dataString.length];

            try {
                for (int i = 0; i < data.length; i++)
                    data[i] = Integer.parseInt(dataString[i]);
            } catch (NumberFormatException e){
                e.printStackTrace();
                return false;
            } catch (IndexOutOfBoundsException e){
                e.printStackTrace();
                return false;
            }

            matchNumber = data[0];
            teamNumber = data[1];
            allianceColor = data[2];

        } catch (IndexOutOfBoundsException e){
            e.printStackTrace();
            return false;
        } catch (Exception e){
            e.printStackTrace();
            return false;
        }
        // only way code can get to this point is if there are no exceptions
        return true;
    }
}
