package com.vandenrobotics.functionfirst.adapter;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.UUID;

import android.bluetooth.*;

/**
 * Created by Joey on 9/23/2014.
 */
public class BtConnectionThread extends Thread {
    private BluetoothSocket mmSocket;
    private BluetoothDevice mmDevice;
    private OutputStream mmOutStream;

    private final UUID MY_UUID = UUID.fromString("ba209999-0c6c-11d2-97cf-00c04f8eea45");

    public BtConnectionThread(BluetoothDevice device){
        BluetoothSocket tmp = null;
        mmDevice = device;

        try{
            tmp = mmDevice.createRfcommSocketToServiceRecord(MY_UUID);
        } catch (IOException e){
            e.printStackTrace();
        }
        mmSocket = tmp;
    }

    public void run() {
        try{
            mmSocket.connect();
            System.out.println("CONNECTED TO SOCKET");
        } catch (IOException connectException){
            try{
                System.out.println("cannot connect to socket");
                mmSocket.close();
            } catch (IOException closeException){
                closeException.printStackTrace();}
            return;
        }

        manageConnectedSocket();
    }

    private void manageConnectedSocket(){
        OutputStream tmpOut = null;

        try{
            tmpOut = mmSocket.getOutputStream();
        } catch (IOException e) {
            e.printStackTrace();
        }

        mmOutStream = tmpOut;
    }

    public void write(File file){
        try{
            FileInputStream f = new FileInputStream(file);
            BufferedReader br = new BufferedReader(new InputStreamReader(f));
            String line;
            while((line=br.readLine())!=null){
                try{
                    line += "\n";
                    mmOutStream.write(line.getBytes());
                } catch (Exception e){
                    e.printStackTrace();
                    break;
                }
            }
            br.close();
            f.close();
        } catch (FileNotFoundException e){
            e.printStackTrace();
        } catch (IOException e){
            e.printStackTrace();
        }
    }

    public void cancel() {
        try{
            mmSocket.close();
        } catch (IOException e){}
    }
}

