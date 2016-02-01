package com.vandenrobotics.functionfirst.dialogs;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v4.app.DialogFragment;
import android.app.Dialog;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.CheckBox;
import android.widget.ToggleButton;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.model.StepStack;

/**
 * Created by Programming701-A on 2/25/2014.
 */
public class EditStepStackDialogFragment extends DialogFragment {

    // Use this instance of the interface to deliver action events
    DialogListener mListener;

    public StepStack mStepStack;

    private ToggleButton[] totes = new ToggleButton[6];
    private CheckBox knockedOver;

    // Override the Fragment.onAttach() method to instantiate the NoticeDialogListener
    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
        // Verify that the host activity implements the callback interface
        try {
            // Instantiate the NoticeDialogListener so we can send events to the host
            mListener = (DialogListener) activity;
        } catch (ClassCastException e) {
            // The activity doesn't implement the interface, throw exception
            throw new ClassCastException(activity.toString()
                    + " must implement DialogListener");
        }
    }

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        // this will inflate the complex dialog view to save the values
        LayoutInflater inflater = getActivity().getLayoutInflater();
        View view = inflater.inflate(R.layout.dialog_edit_stepstack, null);

        assignViews(view);
        loadStepStack(mStepStack);

        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        builder.setTitle(R.string.text_titleEditStack)
                .setView(view)
                .setPositiveButton(R.string.button_ok, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // user clicked OK Button
                        saveStepStack();
                        mListener.onDialogPositiveClick(EditStepStackDialogFragment.this);
                    }
                })
                .setNegativeButton(R.string.button_cancel, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // user cancelled the dialog
                        mListener.onDialogNegativeClick(EditStepStackDialogFragment.this);
                    }
                });
        return builder.create();
    }

    private void assignViews(View view){
        try{
            totes[0] = (ToggleButton)view.findViewById(R.id.toggleCoopStack1);
            totes[1] = (ToggleButton)view.findViewById(R.id.toggleCoopStack2);
            totes[2] = (ToggleButton)view.findViewById(R.id.toggleCoopStack3);
            totes[3] = (ToggleButton)view.findViewById(R.id.toggleCoopStack4);
            totes[4] = (ToggleButton)view.findViewById(R.id.toggleCoopStack5);
            totes[5] = (ToggleButton)view.findViewById(R.id.toggleCoopStack6);
            knockedOver = (CheckBox)view.findViewById(R.id.cb_coopStackKnockedOver);
        } catch (Exception e){
            e.printStackTrace();
            System.out.println("ERROR");
        }
    }

    private void loadStepStack(StepStack stepStack){
        for(int i = 0; i < totes.length; i++){
            totes[i].setChecked(stepStack.mTotes[i]);
        }
        knockedOver.setChecked(stepStack.mKnocked);
    }

    private void saveStepStack(){
        for(int i = 0; i < mStepStack.mTotes.length; i++){
            mStepStack.mTotes[i] = totes[i].isChecked();
        }
        mStepStack.mKnocked = knockedOver.isChecked();
    }
}