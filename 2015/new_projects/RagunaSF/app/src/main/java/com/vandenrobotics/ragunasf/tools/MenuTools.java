package com.vandenrobotics.ragunasf.tools;

import android.app.AlertDialog;
import android.app.FragmentManager;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;

import com.vandenrobotics.ragunasf.R;
import com.vandenrobotics.ragunasf.controllers.dialogs.ConfirmNavigationDialogFragment;

/**
 * Created by Joe on 7/26/15.
 */
public abstract class MenuTools {

    public static void loadWebsite(FragmentManager manager){
        ConfirmNavigationDialogFragment confirmDialog = new ConfirmNavigationDialogFragment();

        Bundle bundle = new Bundle();
        bundle.putString("URL", "www.vandenrobotics.com");

        confirmDialog.setArguments(bundle);
        confirmDialog.show(manager, "confirm navigation");
    }

    public static void about(Context context){
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder .setTitle(context.getResources().getString(R.string.dialog_AboutTitle) + " " + context.getResources().getString(R.string.app_version))
                .setMessage(R.string.dialog_AboutMessage)
                .setPositiveButton(R.string.button_ok, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.dismiss();
                    }
                });
        builder.show();
    }


}
