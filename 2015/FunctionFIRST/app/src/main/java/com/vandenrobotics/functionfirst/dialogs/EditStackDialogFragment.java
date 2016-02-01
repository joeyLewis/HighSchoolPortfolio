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
import android.widget.FrameLayout;
import android.widget.ToggleButton;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.model.Stack;
import com.vandenrobotics.functionfirst.views.NumberPicker;

/**
 * Created by Programming701-A on 2/25/2014.
 */
public class EditStackDialogFragment extends DialogFragment {

    // Use this instance of the interface to deliver action events
    DialogListener mListener;

    public Stack mStack;

    private ToggleButton[] totes = new ToggleButton[6];
    private ToggleButton container;
    private NumberPicker containerHeight;
    private ToggleButton litter;
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
        View view = inflater.inflate(R.layout.dialog_edit_stack, null);

        assignViews(view);
        loadStack(mStack);

        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        builder.setTitle(R.string.text_titleEditStack)
                .setView(view)
                .setPositiveButton(R.string.button_ok, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // user clicked OK Button
                        // save all of the values from the views into the dialog
                        saveStack();
                        mListener.onDialogPositiveClick(EditStackDialogFragment.this);
                    }
                })
                .setNegativeButton(R.string.button_cancel, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // user cancelled the dialog
                        // just run the negative click
                        mListener.onDialogNegativeClick(EditStackDialogFragment.this);
                    }
                });
        return builder.create();
    }

    private void assignViews(View view){
        try{
            totes[0] = (ToggleButton)view.findViewById(R.id.toggleTeleStack1);
            totes[1] = (ToggleButton)view.findViewById(R.id.toggleTeleStack2);
            totes[2] = (ToggleButton)view.findViewById(R.id.toggleTeleStack3);
            totes[3] = (ToggleButton)view.findViewById(R.id.toggleTeleStack4);
            totes[4] = (ToggleButton)view.findViewById(R.id.toggleTeleStack5);
            totes[5] = (ToggleButton)view.findViewById(R.id.toggleTeleStack6);
            containerHeight = (NumberPicker)view.findViewById(R.id.pickerContainerHeight);
            container = (ToggleButton)view.findViewById(R.id.toggleContainer);
            litter = (ToggleButton)view.findViewById(R.id.toggleLitter);
            knockedOver = (CheckBox)view.findViewById(R.id.cb_stackKnockedOver);

            containerHeight.setMinValue(0);
            containerHeight.setMaxValue(6);

        } catch (Exception e){
            e.printStackTrace();
        }
    }

    private void loadStack(Stack stack){
        // loads the values from the stack into the widgets
        for(int i = 0; i < totes.length; i++){
            totes[i].setChecked(stack.mTotes[i]);
        }
        containerHeight.setValue(stack.mContainerHeight);
        container.setChecked(stack.mContainer);
        litter.setChecked(stack.mLitter);
        knockedOver.setChecked(stack.mKnocked);

    }

    private void saveStack() {
        // saves all of the values from the dialog to the stack
        for(int i=0; i < mStack.mTotes.length; i++){
            mStack.mTotes[i] = totes[i].isChecked();
        }
        mStack.mContainerHeight = containerHeight.getValue();
        mStack.mContainer = container.isChecked();
        mStack.mLitter = litter.isChecked();
        mStack.mKnocked = knockedOver.isChecked();
    }
}