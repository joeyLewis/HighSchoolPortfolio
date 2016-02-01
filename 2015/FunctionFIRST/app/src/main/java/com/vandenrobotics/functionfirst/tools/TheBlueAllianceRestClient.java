package com.vandenrobotics.functionfirst.tools;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;

import com.loopj.android.http.*;

import org.apache.http.Header;
import org.apache.http.message.BasicHeader;

/**
 * Created by Programming701-A on 2/1/2015.
 */
public class TheBlueAllianceRestClient {

    public static Header[] GET_HEADER = {new BasicHeader("X-TBA-App-Id", "frc701:scouting-system:dev_v01")};
    private static final String BASE_URL = "http://www.thebluealliance.com/api/v2/";

    private static AsyncHttpClient client = new AsyncHttpClient();

    public static void get(Context context, String url, AsyncHttpResponseHandler responseHandler){
        client.get(context, getAbsoluteUrl(url), GET_HEADER, null, responseHandler);
    }

    public static boolean isOnline(Context context){
        ConnectivityManager cm = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo netInfo = cm.getActiveNetworkInfo();
        return netInfo != null && netInfo.isConnectedOrConnecting();
    }

    private static String getAbsoluteUrl(String relativeUrl){
        return BASE_URL + relativeUrl;
    }

}
