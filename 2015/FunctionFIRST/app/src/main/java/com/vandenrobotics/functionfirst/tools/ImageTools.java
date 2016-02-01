package com.vandenrobotics.functionfirst.tools;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.widget.ImageView;

import com.squareup.picasso.Picasso;
import com.vandenrobotics.functionfirst.R;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.RejectedExecutionHandler;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;


/**
 * Created by Programming701-A on 2/9/2015.
 */
public class ImageTools {

    private static final String BASE_URL = "http://www.chiefdelphi.com/media/img/";

    // download an image from online and turn it into an Image
    public static void downloadImages(ArrayList<JSONArray> all_media, ArrayList<Integer> teamnumbers){
        // grab an image from the url given, and turn it into a bitmap
        BlockingQueue<Runnable> queue = new ArrayBlockingQueue<>(100, true);
        ThreadPoolExecutor executor = new ThreadPoolExecutor(2,4,1,TimeUnit.SECONDS, queue);

        executor.setRejectedExecutionHandler(new RejectedHandler());

        for(int i = 0; i < all_media.size(); i++){
            ArrayList<JSONObject> media;
            ImageDownloadTask imageDownloadTask = null;
            try {
                media = JSONTools.parseJSONArray(all_media.get(i));
                imageDownloadTask = new ImageDownloadTask(media.get(0).getJSONObject("details").getString("image_partial"), teamnumbers.get(i));
            } catch (JSONException e){
                e.printStackTrace();
            }

            try{
                executor.execute(imageDownloadTask);
            } catch (RejectedExecutionException e) {
                e.printStackTrace();
            } catch (NullPointerException e){
                e.printStackTrace();
            }
            try {
                Thread.sleep(30);
            } catch (InterruptedException e){
                e.printStackTrace();
            }

        }
    }

    // access the external storage to grab an image and load it into the provided image view under context
    public static void placeImage(Context context, int teamnumber, ImageView imageView){
        Picasso.with(context)
               .load(ExternalStorageTools.readImage(teamnumber))
               .placeholder(R.drawable.nopic)
               .error(R.drawable.nopic)
               .into(imageView);
    }

    private static String getAbsoluteUrl(String relativeUrl){
        return BASE_URL + relativeUrl;
    }

    private static class ImageDownloadTask implements Runnable {

        private String url;
        private int team_number;

        public ImageDownloadTask(String url, int team_number){
            this.url = url;
            this.team_number = team_number;
        }

        @Override
        public void run() {
            try{
                Thread.sleep(50);
                InputStream inputStream = (InputStream) new URL(getAbsoluteUrl(url)).getContent();
                Bitmap image = BitmapFactory.decodeStream(inputStream);
                inputStream.close();
                ExternalStorageTools.writeImage(image, team_number);
            } catch (IOException e){
                e.printStackTrace();
            } catch (InterruptedException e){
                e.printStackTrace();
            }
        }
    }

    private static class RejectedHandler implements RejectedExecutionHandler {
        @Override
        public void rejectedExecution(Runnable arg0, ThreadPoolExecutor arg1){
            System.err.println(Thread.currentThread().getName() + " execution rejected: " + arg0);
        }
    }
}
