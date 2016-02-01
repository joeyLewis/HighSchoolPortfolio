package com.vandenrobotics.functionfirst.views;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.widget.ImageView;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.model.Stack;
import com.vandenrobotics.functionfirst.model.StepStack;

import java.util.ArrayList;

/**
 * Created by Programming701-A on 3/2/2015.
 */
public class FieldDiagram extends ImageView {

    public ArrayList<Stack> mStacks;
    public ArrayList<StepStack> mStepStacks;
    public Bitmap background;
    public Paint mPaint;

    public FieldDiagram(Context context){
        super(context);
        mStacks = new ArrayList<>();
        mStepStacks = new ArrayList<>();
        mPaint = new Paint();
        mPaint.setStyle(Paint.Style.FILL);
    }

    public FieldDiagram(Context context, AttributeSet attrs){
        super(context, attrs);
        mStacks = new ArrayList<>();
        mStepStacks = new ArrayList<>();
        mPaint = new Paint();
        mPaint.setStyle(Paint.Style.FILL);
    }

    public FieldDiagram(Context context, AttributeSet attrs, int defStyle){
        super(context, attrs, defStyle);
        mStacks = new ArrayList<>();
        mStepStacks = new ArrayList<>();
        mPaint = new Paint();
        mPaint.setStyle(Paint.Style.FILL);
    }

    @Override
    protected void onDraw(Canvas canvas){
        super.onDraw(canvas);
        try {
            for (Stack s : mStacks) {
                String containerText = (s.mContainer) ? "C" : "";
                String litterText = (s.mLitter) ? "L" : "";
                String knockedText = (s.mKnocked) ? "K" : "S";
                String text = (s.mContainer)? s.getTotalTotes() + "/" + s.mContainerHeight + containerText + litterText + "/" + knockedText :
                        s.getTotalTotes() + containerText + litterText + "/" + knockedText;

                float x = (float) getWidth() * s.mPoint.x;
                float y = (float) getHeight() * s.mPoint.y;

                mPaint.setColor(getResources().getColor(R.color.Gray));
                canvas.drawRect(x - 25, (float) (y - 12.5), x + 25, (float) (y + 12.5), mPaint);
                mPaint.setColor(getResources().getColor(R.color.Gold));
                canvas.drawText(text, x-20, y+(float)2.5, mPaint);
            }

            for (StepStack s : mStepStacks) {
                String text = s.getTotalTotes() + "";

                float x = (float) getWidth() * s.mPoint.x;
                float y = (float) getHeight() * s.mPoint.y;

                mPaint.setColor(getResources().getColor(R.color.Gold));
                canvas.drawRect(x - 25, (float) (y - 12.5), x + 25, (float) (y + 12.5), mPaint);
                mPaint.setColor(getResources().getColor(R.color.Gray));
                canvas.drawText(text, x-20, y+(float)2.5, mPaint);
            }
        } catch(Exception e){
            e.printStackTrace();
            setImageDrawable(getResources().getDrawable(R.drawable.field_diagram_red));
        }
    }
}
