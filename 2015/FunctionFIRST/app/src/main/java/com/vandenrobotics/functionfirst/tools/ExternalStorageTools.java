package com.vandenrobotics.functionfirst.tools;

import android.graphics.Bitmap;
import android.os.Environment;

import com.vandenrobotics.functionfirst.model.Match;
import com.vandenrobotics.functionfirst.model.MatchData;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.ArrayList;

/**
 * Created by Programming701-A on 2/7/2015.
 */
public class ExternalStorageTools {

    private static final File BASE_DIR = Environment.getExternalStorageDirectory();

    // writes all events currently downloaded to the file (as a JSONDocument)
    public static void writeEvents(ArrayList<JSONObject> events) {
        JSONArray downloadedEvents = new JSONArray(events);
        if(isExternalStorageWritable()){
            try {
                FileWriter fileWriter = new FileWriter(createFile("ScoutData","events.json"));
                fileWriter.write(downloadedEvents.toString());
                fileWriter.flush();
                fileWriter.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // reads the JSONDocument and returns a JSONArray of events (BASE_DIR)
    public static ArrayList<JSONObject> readEvents(){
        ArrayList<JSONObject> downloadedEvents = new ArrayList<>();

        if(isExternalStorageReadable()){
            try{
                String fileContents = "";
                String line;
                FileInputStream fileInputStream = new FileInputStream(createFile("ScoutData","events.json"));
                BufferedReader br = new BufferedReader(new InputStreamReader(fileInputStream));
                while((line = br.readLine())!=null)
                    fileContents += line;
                br.close();
                fileInputStream.close();

                JSONArray events = new JSONArray(fileContents);
                downloadedEvents = JSONTools.parseJSONArray(events);
            } catch(FileNotFoundException e){
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        return downloadedEvents;
    }

    // writes all teams at an event the file under directory BASE_DIR/event (as a JSONDocument)
    public static void writeTeams(ArrayList<JSONObject> teams, String event){
        JSONArray presentTeams = new JSONArray(teams);
        if(isExternalStorageWritable()){
            try {
                FileWriter fileWriter = new FileWriter(createFile("ScoutData/"+event,"teams.json"));
                fileWriter.write(presentTeams.toString());
                fileWriter.flush();
                fileWriter.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // reads the JSONDocument and returns a JSONArray of teams (from a certain event (BASE_DIR/event)
    public static ArrayList<JSONObject> readTeams(String event){
        ArrayList<JSONObject> teams = new ArrayList<>();

        if(isExternalStorageReadable()){
            try{
                String fileContents = "";
                String line;
                FileInputStream fileInputStream = new FileInputStream(createFile("ScoutData/"+event,"teams.json"));
                BufferedReader br = new BufferedReader(new InputStreamReader(fileInputStream));
                while((line = br.readLine())!=null)
                    fileContents += line;
                br.close();
                fileInputStream.close();

                JSONArray events = new JSONArray(fileContents);
                teams = JSONTools.parseJSONArray(events);
            } catch(FileNotFoundException e){
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        return teams;
    }

    public static void writeImage(Bitmap image, int team_number){
        if(isExternalStorageWritable()){
            try {
                FileOutputStream fileOutputStream = new FileOutputStream(createFile("ScoutData/Images", team_number+".png"));
                image.compress(Bitmap.CompressFormat.PNG, 100, fileOutputStream);
                fileOutputStream.flush();
                fileOutputStream.close();
            } catch (IOException e){
                e.printStackTrace();
            }
        }
    }

    public static File readImage(int team_number){
        return createFile("ScoutData/Images", team_number + ".png");
    }

    // writes the device number to the event directory
    public static void writeDevice(int device, String event){
        if(isExternalStorageWritable()){
            try {
                FileWriter fileWriter = new FileWriter(createFile("ScoutData/"+event,"device.txt"));
                fileWriter.write(device+"");
                fileWriter.flush();
                fileWriter.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // reads the device number from the event directory
    public static int readDevice(String event){
        int dNum = 0;
        if(isExternalStorageReadable()){
            try{
                FileInputStream fileInputStream = new FileInputStream(createFile("ScoutData/"+event, "device.txt"));
                BufferedReader br = new BufferedReader(new InputStreamReader(fileInputStream));
                dNum = Integer.parseInt(br.readLine());
                br.close();
                fileInputStream.close();
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (NumberFormatException e) {
                e.printStackTrace();
            }
        }
        return (dNum>0 && dNum<=6)? dNum : 1;
    }

    // writes the currentMatch to the event / device number directory
    public static void writeCurrentMatch(int match, String event, int device){
        if(isExternalStorageWritable()){
            try {
                FileWriter fileWriter = new FileWriter(createFile("ScoutData/"+event+"/"+getDeviceString(device),"savedmatch.txt"));
                fileWriter.write(match+"");
                fileWriter.flush();
                fileWriter.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // reads the currentMatch from the event / device number directory
    public static int readCurrentMatch(String event, int device){
        int mNum = 0;
        if(isExternalStorageReadable()) {
            try {
                FileInputStream fileInputStream = new FileInputStream(createFile("ScoutData/"+event + "/" + getDeviceString(device), "savedmatch.txt"));
                BufferedReader br = new BufferedReader(new InputStreamReader(fileInputStream));
                mNum = Integer.parseInt(br.readLine());
                br.close();
                fileInputStream.close();
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (NumberFormatException e) {
                e.printStackTrace();
            }
        }
        return (mNum >0)? mNum : 1;
    }

    // creates a txt file matchlist out of the ArrayList of matches
    public static void writeMatches(ArrayList<Match> matches, String event){
        if(isExternalStorageWritable()){
            try{
                FileWriter fileWriter = new FileWriter(createFile("ScoutData/"+event, "matchlist.txt"));
                for(int i = 0; i < matches.size(); i++){
                    fileWriter.write(matches.get(i).toString());
                }
                fileWriter.flush();
                fileWriter.close();
            } catch (IOException e){
                e.printStackTrace();
            }
        }
    }

    // reads the text-file matchlist and creates a matchlist to return
    public static ArrayList<Match> readMatches(String event){
        ArrayList<Match> matches = new ArrayList<>();
        if(isExternalStorageReadable()){
            try{
                String line;
                FileInputStream fileInputStream = new FileInputStream(createFile("ScoutData/"+event,"matchlist.txt"));
                BufferedReader br = new BufferedReader(new InputStreamReader(fileInputStream));
                while((line = br.readLine())!=null)
                    matches.add(new Match(line));
                br.close();
                fileInputStream.close();

            } catch(FileNotFoundException e){
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        return matches;
    }

    // writes a JSONDocument data file out of MatchData to the event/device directory
    public static void writeData(ArrayList<MatchData> matchData, String event, int device){
        if(isExternalStorageWritable()) {
            try {
                FileWriter fileWriter = new FileWriter(createFile("ScoutData/" + event + "/device" + device, "data.txt"));
                for (int i = 0; i < matchData.size(); i++) {
                    fileWriter.append(matchData.get(i).toString() + "\n");
                }
                fileWriter.flush();
                fileWriter.close();
            } catch (IOException e){
                e.printStackTrace();
            }
        }
    }

    public static void writeData(MatchData matchData, String event, int device){
        if(isExternalStorageWritable()) {
            try {
                FileWriter fileWriter = new FileWriter(createFile("ScoutData/" + event + "/device" + device, "data.txt"), true);
                fileWriter.append(matchData.toString() + "\n\r");
                fileWriter.flush();
                fileWriter.close();
            } catch (IOException e){
                e.printStackTrace();
            }
        }
    }

    // reads the JSONDocument data file in to the device and into a MatchData value
    public static ArrayList<MatchData> readData(String event, int   device){
        ArrayList<MatchData> matchData = new ArrayList<>(200);
        if(isExternalStorageReadable()) {
            try {
                String line;
                FileInputStream fileInputStream = new FileInputStream(createFile("ScoutData/" + event + "/device" + device, "data.txt"));
                BufferedReader br = new BufferedReader(new InputStreamReader(fileInputStream));
                while ((line = br.readLine()) != null) {
                    try {
                        String[] lineSections = line.split("\\$");
                        String[] initData = lineSections[0].split(",");
                        int match = Integer.parseInt(initData[0]) - 1;
                        matchData.add(match, new MatchData(line));
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
            return matchData;
    }

    public static boolean isExternalStorageWritable() {
        String state = Environment.getExternalStorageState();
        return Environment.MEDIA_MOUNTED.equals(state);
    }

    public static boolean isExternalStorageReadable() {
        String state = Environment.getExternalStorageState();
        return (Environment.MEDIA_MOUNTED.equals(state) ||
                Environment.MEDIA_MOUNTED_READ_ONLY.equals(state));
    }

    public static File createDirectory(String dir){
        File f = new File(BASE_DIR.getAbsolutePath() + "/" + dir);
        if(!f.exists())
            f.mkdirs();
        return f;
    }

    public static File createFile(String dir, String filename){
        File path = createDirectory(dir);
        File f = new File(path, filename);
        if(!f.exists())
            try {
                f.createNewFile();
            } catch (IOException e){
                e.printStackTrace();
            }
        return f;
    }

    public static void deleteFiles(String dir){
        deleteDirectory(new File(BASE_DIR.getAbsolutePath()+"/ScoutData/"+dir));
    }
    public static boolean deleteDirectory(File path) {
        if( path.exists() ) {
            File[] files = path.listFiles();
            if (files == null) {
                return true;
            }
            for(int i=0; i<files.length; i++) {
                if(files[i].isDirectory()) {
                    deleteDirectory(files[i]);
                }
                else {
                    files[i].delete();
                }
            }
        }
        return( path.delete() );
    }

    private static String getDeviceString(int device){
        return ((device<4) ? "Red"+device : "Blue"+(device-3));
    }

}
