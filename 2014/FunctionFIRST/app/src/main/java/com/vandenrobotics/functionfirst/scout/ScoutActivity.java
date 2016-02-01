package com.vandenrobotics.functionfirst.scout;

import com.vandenrobotics.functionfirst.R;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.Set;

import android.os.Bundle;
import android.os.Environment;
import android.app.Activity;
import android.bluetooth.*;
import android.content.Context;
import android.content.Intent;

import com.vandenrobotics.functionfirst.adapter.BtConnectionThread;
import com.vandenrobotics.functionfirst.scout.model.MatchData;
import com.vandenrobotics.functionfirst.scout.model.TeamList;

public class ScoutActivity extends Activity {


	public static int deviceNumber = readDevice();
	public static int mCurMatch = readMatch();
	// eventually call readMatches to read the matchlist and create a TeamList map
	public static TeamList[] mTeamList = new TeamList[200]; //readMatches();
	public static MatchData[] mMatchResults = readData();
	public static int maxMatches = readMatches();
	
	public static int REQUEST_ENABLE_BT = 1;
	
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_scout);
	}
	
	@Override
	protected void onResume(){
		super.onResume();
		mCurMatch = readMatch();
		Intent intent = new Intent(this, MatchActivity.class);
		intent.putExtra("matchNumber", mCurMatch);
		intent.putExtra("teamNumber",mTeamList[mCurMatch-1].teams[deviceNumber-1]);
		intent.putExtra("deviceNumber", deviceNumber);
		startActivity(intent);
		onDestroy();
	}
	
	public static Intent goToMatch(Context context, int curMatch, int newMatch, int dNum, MatchData mMatchData){
		
		// write old stuff
		mMatchResults[curMatch-1] = mMatchData;
		writeData();

		mCurMatch = (newMatch>0 && newMatch<=maxMatches)? newMatch : curMatch;
		writeMatch(mCurMatch);
		
		// setup new device and data
		deviceNumber = dNum;
		writeDevice(deviceNumber);
		mMatchResults = readData();	 // update data to ensure that device is the same or if it has changed to load new data
		writeMatch(mCurMatch);
		// start the new MatchActivity
		Intent intent = new Intent(context,MatchActivity.class);
		intent.putExtra("matchNumber", mCurMatch);
		intent.putExtra("teamNumber",mTeamList[mCurMatch-1].teams[deviceNumber-1]);
		intent.putExtra("deviceNumber",deviceNumber);
    	return intent;
	}
	
	public static MatchData[] readData(){
		MatchData[] mMD = new MatchData[200];
		
		File root = Environment.getExternalStorageDirectory();
		File dir = new File(root.getAbsolutePath()+ "/ScoutData/device-" + deviceNumber);
		dir.mkdirs();
		
		File file = new File(dir,"data.txt");

		try{
			FileInputStream f = new FileInputStream(file);
			BufferedReader br = new BufferedReader(new InputStreamReader(f));
			String line;
			while((line=br.readLine())!=null){
				try{
					String[] lineSections = line.split("\\$");
					System.out.println(lineSections[0]);
					String[] initData = lineSections[0].split(",");
					System.out.println(initData[0]);
					int match = Integer.parseInt(initData[0])-1;
					System.out.println("MATCH NUMBER: " + match);
					mMD[match] = new MatchData();
					mMD[match].fromString(line);
				} catch (Exception e){
					e.printStackTrace();
				}
			}
			br.close();
			f.close();
		} catch (FileNotFoundException e){
				e.printStackTrace();
		} catch (IOException e){
			e.printStackTrace();
		}
		return mMD;
	}
	
	public static void writeData(){
		// write data to local directory
		File root = Environment.getExternalStorageDirectory();
		File dir = new File(root.getAbsolutePath()+ "/ScoutData/device-" + deviceNumber);
		dir.mkdirs();
		
		File file = new File(dir,"data.txt");
		try{
			FileOutputStream f = new FileOutputStream(file);
			PrintWriter pw = new PrintWriter(f);
			for(int i = 0; i < mMatchResults.length; i++){
				if(mMatchResults[i]!=null){
					pw.write(mMatchResults[i].toString()+"\r\n");
					System.out.println(mMatchResults[i].toString());
				}
			}
			pw.flush();
			pw.close();
			f.close();
		} catch (FileNotFoundException e){
			e.printStackTrace();
		} catch (IOException e){
			e.printStackTrace();
		}
		
		BtConnectionThread mBtThread = null;
		// attempt to send data by Bluetooth Connection
		try{
			BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
			if(mBluetoothAdapter == null){
				// device does not support bluetooth
				return;
			}
			
			if(!mBluetoothAdapter.isEnabled()){
				// for now, user must enable bluetooth beforehand, not going to ask every match
				return;
			}
			
			Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
			if(pairedDevices.size()>0){
				for(BluetoothDevice device : pairedDevices){
					System.out.println(device.getAddress());
					if(device.getAddress().equals("A4:DB:30:A8:80:44"))
					{
						mBtThread = new BtConnectionThread(device);
						System.out.println("FOUND BT DEVICE");
						break;
					}
				}
			}
			
			mBtThread.run();
			mBtThread.write(file);
			
		} catch (Exception e){
			e.printStackTrace();
		}
	}
	
	public static int readMatches(){
		File root = Environment.getExternalStorageDirectory();
		File dir = new File(root.getAbsolutePath() + "/ScoutData");
		dir.mkdirs();
		File file = new File(dir,"matches.txt");
		int i = 0;
		try{	
			FileInputStream f = new FileInputStream(file);
			BufferedReader br = new BufferedReader(new InputStreamReader(f));
			String line;
			while ((line = br.readLine())!=null){
				String[] teams = line.split(",");
				mTeamList[i] = new TeamList();
				mTeamList[i].matchNumber = Integer.parseInt(teams[0]);
				mTeamList[i].teams[0] = Integer.parseInt(teams[1]);
				mTeamList[i].teams[1] = Integer.parseInt(teams[2]);
				mTeamList[i].teams[2] = Integer.parseInt(teams[3]);
				mTeamList[i].teams[3] = Integer.parseInt(teams[4]);
				mTeamList[i].teams[4] = Integer.parseInt(teams[5]);
				mTeamList[i].teams[5] = Integer.parseInt(teams[6]);
				i++;	
			}
			br.close();
			f.close();
		} catch (FileNotFoundException e){
			e.printStackTrace();
		} catch (IOException e){
			e.printStackTrace();
		}
		return i;
	}
	
	public static void writeDevice(int dNum){
		File root = Environment.getExternalStorageDirectory();
		File dir = new File(root.getAbsolutePath() + "/ScoutData");
		dir.mkdirs();
		File file = new File(dir,"device.txt");
		
		try{
			FileOutputStream f = new FileOutputStream(file);
			PrintWriter pw = new PrintWriter(f);
			pw.println(dNum);
			pw.flush();
			pw.close();
			f.close();
		} catch (FileNotFoundException e){
			e.printStackTrace();
		} catch (IOException e){
			e.printStackTrace();
		}
	}
	
	public static int readDevice(){
		File root = Environment.getExternalStorageDirectory();
		File dir = new File(root.getAbsolutePath() + "/ScoutData");
		dir.mkdirs();
		File file = new File(dir,"device.txt");
		int dNum = 0;
		try{	
			FileInputStream f = new FileInputStream(file);
			BufferedReader br = new BufferedReader(new InputStreamReader(f));
			dNum = Integer.parseInt(br.readLine());
			br.close();
			f.close();
		} catch (FileNotFoundException e){
			e.printStackTrace();
		} catch (IOException e){
			e.printStackTrace();
		} catch (NumberFormatException e){
			e.printStackTrace();
			dNum = 1;
		}
		return (dNum>0 && dNum<7)? dNum : 1;
	}
	
	public static void writeMatch(int match){
		File root = Environment.getExternalStorageDirectory();
		File dir = new File(root.getAbsolutePath() + "/ScoutData/device-" + deviceNumber);
		dir.mkdirs();
		File file = new File(dir,"savedmatch.txt");
		
		try{
			FileOutputStream f = new FileOutputStream(file);
			PrintWriter pw = new PrintWriter(f);
			pw.println(match);
			pw.flush();
			pw.close();
			f.close();
		} catch (FileNotFoundException e){
			e.printStackTrace();
		} catch (IOException e){
			e.printStackTrace();
		}
	}
	
	public static int readMatch(){
		File root = Environment.getExternalStorageDirectory();
		File dir = new File(root.getAbsolutePath() + "/ScoutData/device-" + deviceNumber);
		dir.mkdirs();
		File file = new File(dir,"savedmatch.txt");
		int mNum = 0;
		try{	
			FileInputStream f = new FileInputStream(file);
			BufferedReader br = new BufferedReader(new InputStreamReader(f));
			mNum = Integer.parseInt(br.readLine());
			br.close();
			f.close();
		} catch (FileNotFoundException e){
			e.printStackTrace();
			mNum = 1;
		} catch (IOException e){
			e.printStackTrace();
			mNum = 1;
		} catch (NumberFormatException e){
			e.printStackTrace();
			mNum = 1;
		}
		return (mNum>0 && mNum<=maxMatches)? mNum : 1;
	}
}
