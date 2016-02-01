package com.vandenrobotics.ragunasf.tools;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

/**
 * Created by Programming701-A on 2/7/2015.
 */
public abstract class JSONTools {

    public static ArrayList<JSONObject> parseJSONArray(JSONArray jsonArray) throws JSONException {
        ArrayList<JSONObject> jsonObjects = new ArrayList<>();
        for (int i = 0; i < jsonArray.length(); i++)
            jsonObjects.add(jsonArray.getJSONObject(i));
        return jsonObjects;
    }
}
