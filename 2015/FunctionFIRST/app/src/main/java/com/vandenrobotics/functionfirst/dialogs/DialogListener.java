package com.vandenrobotics.functionfirst.dialogs;

import android.support.v4.app.DialogFragment;

/**
 * Created by Programming701-A on 12/22/2014.
 */
public interface DialogListener {
    public void onDialogPositiveClick(DialogFragment dialog);
    public void onDialogNegativeClick(DialogFragment dialog);
}
