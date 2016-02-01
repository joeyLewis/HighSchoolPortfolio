package com.vandenrobotics.ragunasf.tools;

import android.content.Context;
import android.widget.ImageView;

import com.squareup.picasso.Picasso;
import com.vandenrobotics.ragunasf.R;

/**
 * Created by Programming701-A on 2/9/2015.
 */
public abstract class ImageTools {

    // access the external storage to grab an image and load it into the provided image view under context
    public static void placeImage(Context context, int teamNumber, ImageView imageView){
        Picasso.with(context)
                .load(ExternalStorageTools.readImage(teamNumber))
                .placeholder(R.drawable.icon_nopic)
                .error(R.drawable.icon_nopic)
                .into(imageView);
    }
}
