package com.vandenrobotics.ragunasf.adapters;

import android.content.Context;
import android.database.DataSetObservable;
import android.database.DataSetObserver;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.ImageView;
import android.widget.ListAdapter;
import android.widget.TextView;

import com.vandenrobotics.ragunasf.R;
import com.vandenrobotics.ragunasf.model.Team;
import com.vandenrobotics.ragunasf.tools.ImageTools;

import java.util.ArrayList;
import java.util.List;

/**
 * TeamListAdapter handles updating the teamlist and displaying a filterable list of teams in a ListView
 */
public class TeamListAdapter implements ListAdapter, Filterable {

    private DataSetObservable mDataSetObservable = new DataSetObservable();

    private LayoutInflater mInflater;
    private TeamFilter mFilter;

    private List<Team> mFilteredTeamList;
    private List<Team> mTeamList;

    public TeamListAdapter(Context context, List<Team> teamList) {
        init(context, teamList);
    }

    private void init(Context context, List<Team> teamList) {
        mInflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        mFilteredTeamList = mTeamList = teamList;
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
        return mFilteredTeamList.size();
    }

    @Override
    public Team getItem(int position) {
        return mFilteredTeamList.get(position);
    }

    public int getPosition(Team team){
        for(int i = 0; i < mFilteredTeamList.size(); i++){
            if(team == mFilteredTeamList.get(i)){
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
        public ImageView teamImage;
        public TextView teamNumber;
        public TextView teamNickname;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Holder holder;
        if (convertView == null) {
            convertView = mInflater.inflate(R.layout.team_list_item, null);

            holder = new Holder();
            holder.teamImage = (ImageView) convertView.findViewById(R.id.teamImage);
            holder.teamNumber = (TextView) convertView.findViewById(R.id.teamNumber);
            holder.teamNickname = (TextView) convertView.findViewById(R.id.teamNickname);

            convertView.setTag(holder);
        } else {
            holder = (Holder) convertView.getTag();
        }
        Team team = getItem(position);

        ImageTools.placeImage(parent.getContext(), team.getNumber(), holder.teamImage);
        holder.teamNumber.setText("Team " + String.valueOf(team.getNumber()));
        holder.teamNickname.setText(team.getNickname());

        return convertView;
    }

    @Override
    public Filter getFilter() {
        if (mFilter == null) {
            mFilter = new TeamFilter();
        }
        return mFilter;
    }

    private class TeamFilter extends Filter {

        @Override
        protected FilterResults performFiltering(CharSequence constraint) {
            FilterResults filterResults = new FilterResults();
            if (constraint == null || constraint.length() == 0) {
                filterResults.values = mTeamList;
                filterResults.count = mTeamList.size();
            } else {
                final String lastToken = constraint.toString().toLowerCase();
                final int count = mTeamList.size();
                final List<Team> list = new ArrayList<>();
                Team team;

                for (int i = 0; i < count; i++) {
                    team = mTeamList.get(i);
                    if (team.getNickname().toLowerCase().contains(lastToken)
                            || String.valueOf(team.getNumber()).contains(lastToken)){
                        list.add(team);
                    }
                }

                filterResults.values = list;
                filterResults.count = list.size();
            }
            return filterResults;
        }

        @Override
        protected void publishResults(CharSequence constraint, FilterResults results) {
            mFilteredTeamList = (List<Team>) results.values;
            if (results.count > 0) {
                notifyDataSetChanged();
            } else {
                notifyDataSetInvalidated();
            }
        }

    }

}
