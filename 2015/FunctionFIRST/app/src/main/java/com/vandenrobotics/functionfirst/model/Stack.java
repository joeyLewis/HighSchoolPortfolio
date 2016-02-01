package com.vandenrobotics.functionfirst.model;

import android.graphics.PointF;

/**
 * Created by Programming701-A on 2/21/2015.
 */
public class Stack {

    public PointF mPoint;
    public boolean[] mTotes;        // takes values 0 for no tote, 1 for tote stacked width-wise, 2 for tote stacked length-wise
                                // takes values 3 for tote upside down width-wise, 4 for tote upside down length-wise
                                // this allows us to track: number of totes contributed to stack, level of top tote, orientation
    public boolean mContainer;      // takes values 0 for no container, 1 for container stacked upright, 2 for container stacked sideways, 3 container upside down
    public int mContainerHeight;// takes the value of the number of totes under the container when stacked (if this robot stacked the container), otherwise -1
    public boolean mLitter;         // takes values 0 for not litter, 1 for litter loaded normal, 2 for litter loaded
    public boolean mKnocked;    // takes values 0 for no, 1 for this robot knocked over this stack

    public Stack(){
        mPoint = new PointF();
        mTotes = new boolean[6];
        mContainer = false;
        mContainerHeight = 0;
        mLitter = false;
        mKnocked = false;
    }

    public Stack(Stack stack){
        this();

        mPoint = stack.mPoint;
        mTotes = stack.mTotes;
        mContainer = stack.mContainer;
        mContainerHeight = stack.mContainerHeight;
        mLitter = stack.mLitter;
        mKnocked = stack.mKnocked;
    }

    public Stack(String s){
        this();

        try {
            String[] dataString = s.split(",");
            float[] data = new float[dataString.length];

            for(int i = 0; i < data.length; i++){
                data[i] = Float.parseFloat(dataString[i]);
            }

            int index = 0;

            mPoint.x = data[index];
            index++;
            mPoint.y = data[index];
            index++;

            for(int i = 0; i < mTotes.length; i++){
                mTotes[i] = ((int)data[index]==1);
                index++;
            }

            mContainer = ((int)data[index]==1);
            index++;
            mContainerHeight = (int)data[index];
            index++;
            mLitter = ((int)data[index]==1);
            index++;
            mKnocked = ((int)data[index]==1);

        } catch (Exception e){
            e.printStackTrace();
        }
    }

    @Override
    public String toString(){
        int[] tempTotes = new int[mTotes.length];
        for(int i = 0; i < tempTotes.length; i++){
            tempTotes[i] = (mTotes[i])? 1 : 0;
        }
        int tempContainer = mContainer? 1 : 0;
        int tempLitter = mLitter? 1 : 0;
        int tempKnocked = mKnocked? 1 : 0;

        return mPoint.x+","+mPoint.y+","+
               tempTotes[0]+","+tempTotes[1]+","+
               tempTotes[2]+","+tempTotes[3]+","+
               tempTotes[4]+","+tempTotes[5]+","+
               tempContainer+","+mContainerHeight+","+
               tempLitter+","+tempKnocked;
    }

    public int getTotalTotes(){
        int count = 0;
        for(int i = mTotes.length-1; i >= 0; i--){
            if(mTotes[i]) count++;
        }
        return count;
    }
}
