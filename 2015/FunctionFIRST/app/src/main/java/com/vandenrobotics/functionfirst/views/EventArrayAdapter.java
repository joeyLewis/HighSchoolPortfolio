package com.vandenrobotics.functionfirst.views;


import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;


import android.content.Context;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.SectionIndexer;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

public class EventArrayAdapter extends ArrayAdapter<JSONObject> implements SectionIndexer {

    private ArrayList<JSONObject> itemList;
    private Context context;
    private static String[] sections = {"WK1", "WK2", "WK3", "WK4", "WK5", "WK6", "WK7", "CMP"};
    private static final SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
    private static final Date[] sectionDates = {new Date(115,1,25), new Date(115,2,4),
                                                new Date(115,2,11), new Date(115,2,18),
                                                new Date(115,2,25), new Date(115,3,1),
                                                new Date(115,3,8), new Date(115,3,21)};
    // date formatting is weird, these dates correspond to February, March, and April of 2015
    // int 1: current year - 1900
    // int 2: current month - 1
    // int 3: current day of month

    public EventArrayAdapter(ArrayList<JSONObject> itemList, Context ctx) {
        super(ctx, android.R.layout.simple_list_item_2, android.R.id.text1, itemList);
        this.itemList = itemList;
        this.context = ctx;
    }

    public int getCount() {
        return itemList.size();
    }

    public JSONObject getItem(int position) {
        return itemList.get(position);
    }

    public long getItemId(int position) {
        return itemList.get(position).hashCode();
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent){
        View view = super.getView(position, convertView, parent);
        TextView text1 = (TextView) view.findViewById(android.R.id.text1);
        TextView text2 = (TextView) view.findViewById(android.R.id.text2);

        try {
            text1.setText(itemList.get(position).getString("name"));
            text2.setText("Start Date: " + itemList.get(position).getString("start_date"));
        } catch (JSONException e){
            e.printStackTrace();
        }
        return view;
    }

    @Override
    public int getPositionForSection(int section) {
        Log.d("ListView", "Get position for section");
        try {
            for (int i=0; i < this.getCount(); i++) {
                String item = this.getItem(i).getString("start_date");
                Date eventStart = format.parse(item);
                if (eventStart.equals(sectionDates[section]))
                    return i;
            }
        } catch(JSONException e){
            e.printStackTrace();
        } catch(ParseException e){
            e.printStackTrace();
        }
        return 0;
    }

    @Override
    public int getSectionForPosition(int arg0) {
        Log.d("ListView", "Get section");
        return 0;
    }

    @Override
    public Object[] getSections() {
        Log.d("ListView", "Get sections");
        return sections;
    }

}
