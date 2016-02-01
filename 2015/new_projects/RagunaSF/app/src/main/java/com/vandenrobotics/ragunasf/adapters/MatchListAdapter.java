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

import com.vandenrobotics.ragunasf.R;
import com.vandenrobotics.ragunasf.model.Match;

import java.util.ArrayList;
import java.util.List;

/**
 * MatchListAdapter class handles updating the matchlist and displaying in a filterable ListView
 */

public class MatchListAdapter implements ListAdapter, Filterable {

    private DataSetObservable mDataSetObservable = new DataSetObservable();

    private LayoutInflater mInflater;
    private MatchFilter mFilter;

    private List<Match> mFilteredMatchList;
    private List<Match> mMatchList;

    public MatchListAdapter(Context context, List<Match> matchList) {
        init(context, matchList);
    }

    private void init(Context context, List<Match> matchList) {
        mInflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        mFilteredMatchList = mMatchList = matchList;
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
        return mFilteredMatchList.size();
    }

    @Override
    public Match getItem(int position) {
        return mFilteredMatchList.get(position);
    }

    public int getPosition(Match match){
        for(int i = 0; i < mFilteredMatchList.size(); i++){
            if(match == mFilteredMatchList.get(i)){
                return i;
            }
        }
        return -1;
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
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Holder holder;
        if (convertView == null) {
            convertView = mInflater.inflate(R.layout.match_list_item, null);

            holder = new Holder();
            holder.textView1 = (TextView) convertView.findViewById(R.id.text);

            convertView.setTag(holder);
        } else {
            holder = (Holder) convertView.getTag();
        }
        Match match = getItem(position);

        holder.textView1.setText(match.getListDetails());

        return convertView;
    }

    @Override
    public Filter getFilter() {
        if (mFilter == null) {
            mFilter = new MatchFilter();
        }
        return mFilter;
    }

    /**
     * MatchFilter class which handles searching through the list of matches
     */
    private class MatchFilter extends Filter {

        @Override
        protected FilterResults performFiltering(CharSequence constraint) {
            FilterResults filterResults = new FilterResults();
            if (constraint == null || constraint.length() == 0) {
                filterResults.values = mMatchList;
                filterResults.count = mMatchList.size();
            } else {
                final String lastToken = constraint.toString().toLowerCase();
                final int count = mMatchList.size();
                final List<Match> list = new ArrayList<>();
                Match match;

                for (int i = 0; i < count; i++) {
                    match = mMatchList.get(i);
                    if (match.getListDetails().toLowerCase().contains(lastToken)){
                        list.add(match);
                    }
                }

                filterResults.values = list;
                filterResults.count = list.size();
            }
            return filterResults;
        }

        @Override
        protected void publishResults(CharSequence constraint, FilterResults results) {
            mFilteredMatchList = (List<Match>) results.values;
            if (results.count > 0) {
                notifyDataSetChanged();
            } else {
                notifyDataSetInvalidated();
            }
        }

    }

}
