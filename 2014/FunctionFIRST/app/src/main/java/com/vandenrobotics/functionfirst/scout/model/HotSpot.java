package com.vandenrobotics.functionfirst.scout.model;

import android.graphics.Point;
/**
 * Created by Joey on 9/23/2014.
 */
public class HotSpot extends Point{
    public int type;
    public double x;
    public double y;

    public HotSpot(int type1, double x1, double y1){
        x = x1;
        y = y1;
        type = type1;
    }
}
