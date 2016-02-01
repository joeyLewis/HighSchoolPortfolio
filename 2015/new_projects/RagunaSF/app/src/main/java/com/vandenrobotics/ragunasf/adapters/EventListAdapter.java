package com.vandenrobotics.ragunasf.adapters;

import android.content.Context;
import android.database.DataSetObservable;
import android.database.DataSetObserver;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.ListAdapter;
import android.widget.TextView;

import com.vandenrobotics.ragunasf.model.Event;

import java.util.ArrayList;
import java.util.List;

/**
 * EventListAdapter class handles updating the EventList and displaying a filterable list of events in a ListView
 */
public class EventListAdapter implements ListAdapter, Filterable {

    private DataSetObservable mDataSetObservable = new DataSetObservable();

    private LayoutInflater mInflater;
    private EventFilter mFilter;

    private List<Event> mFilteredEventList;
    private List<Event> mEventList;

    public EventListAdapter(Context context, List<Event> eventList) {
        init(context, eventList);
    }

    private void init(Context context, List<Event> eventList) {
        mInflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        mFilteredEventList = mEventList = eventList;
    }

    @Override
    public void registerDataSetObserver(DataSetObserver observer) {
        mDataSetObservable.registerObserver(observer);
    }

    @Override
    public void unregisterDataSetObserver(DataSetObserver observer) {
        mDataSetObservable.unregisterObserver(observer);
    }

    public void notifyDataSetChanged() {
        mDataSetObservable.notifyChanged();
    }

    public void notifyDataSetInvalidated() {
        mDataSetObservable.notifyInvalidated();
    }

    @Override
    public boolean isEmpty() {
        return getCount()==0;
    }

    @Override
    public boolean areAllItemsEnabled() {
        return true;
    }

    @Override
    public boolean isEnabled(int position) {
        return true;
    }

    @Override
    public int getCount() {
        return mFilteredEventList.size();
    }

    @Override
    public Event getItem(int position) {
        return mFilteredEventList.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public boolean hasStableIds() {
        return false;
    }

    @Override
    public int getItemViewType(int position) {
        return 0;
    }

    @Override
    public int getViewTypeCount() {
        return 1;
    }

    private static class Holder {
        public TextView textView1;
        public TextView textView2;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Holder holder;
        if (convertView == null) {
            convertView = mInflater.inflate(android.R.layout.simple_list_item_2, null);

            holder = new Holder();
            holder.textView1 = (TextView) convertView.findViewById(android.R.id.text1);
            holder.textView2 = (TextView) convertView.findViewById(android.R.id.text2);

            convertView.setTag(holder);
        } else {
            holder = (Holder) convertView.getTag();
        }
        Event event = getItem(position);

        holder.textView1.setText(event.getName());
        holder.textView2.setText(event.getLocation());

        return convertView;
    }

    @Override
    public Filter getFilter() {
        if (mFilter == null) {
            mFilter = new EventFilter();
        }
        return mFilter;
    }

    private class EventFilter extends Filter {

        @Override
        protected FilterResults performFiltering(CharSequence constraint) {
            FilterResults filterResults = new FilterResults();
            if (constraint == null || constraint.length() == 0) {
                filterResults.values = mEventList;
                filterResults.count = mEventList.size();
            } else {
                final String lastToken = constraint.toString().toLowerCase();
                final int count = mEventList.size();
                final List<Event> list = new ArrayList<>();
                Event event;

                for (int i = 0; i < count; i++) {
                    event = mEventList.get(i);
                    if (event.getName().toLowerCase().contains(lastToken)
                            || event.getLocation().toLowerCase().contains(lastToken)){
                        list.add(event);
                    }
                }

                filterResults.values = list;
                filterResults.count = list.size();
            }
            return filterResults;
        }

        @Override
        protected void publishResults(CharSequence constraint, FilterResults results) {
            mFilteredEventList = (List<Event>) results.values;
            if (results.count > 0) {
                notifyDataSetChanged();
            } else {
                notifyDataSetInvalidated();
            }
        }

    }

}
