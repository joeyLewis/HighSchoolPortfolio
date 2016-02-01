package com.vandenrobotics.functionfirst.scout;

import java.util.ArrayList;

import com.vandenrobotics.functionfirst.R;
import com.vandenrobotics.functionfirst.scout.model.HotSpot;
import com.vandenrobotics.functionfirst.scout.model.TeleData;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Paint.Style;
import android.graphics.PointF;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

public class TeleFragment extends Fragment {

	private Button buttonUndo;
	private Button buttonRedo;
	private TextView intakeTime;
	private Button buttonRecord;
	private Button buttonLowScoreDown;
	private Button buttonLowScoreUp;
	private EditText lowScore;
	private Button buttonTruss;
	private Button buttonCatch;
	private Button buttonGoal;
	private Button buttonGiveAssist;
	private Button buttonReceiveAssist;
	private ImageView fieldDiagram;
	
	private boolean recording = false;
	private ArrayList<Double> intakeTimes = new ArrayList<Double>();
	private ArrayList<HotSpot> hotSpots = new ArrayList<HotSpot>();
	private ArrayList<HotSpot> backOrder = new ArrayList<HotSpot>();
	private int hSpotType = 0;
	
	private boolean viewsAssigned = false;
	
	private TeleData mTeleData;
	
	public static TeleFragment newInstance(TeleData teleData){
		TeleFragment tf = new TeleFragment();
		
		Bundle args = new Bundle();
		args.putParcelable("TeleData",teleData);
		
		tf.setArguments(args);
		
		return tf;
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
							 Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.fragment_scout_tele, container, false);
		
		Bundle args = getArguments();
		mTeleData = args.getParcelable("TeleData");
		
		if(viewsAssigned) loadData(mTeleData);
		
		return rootView;
	}
	
	@Override
	public void onViewCreated(View view, Bundle savedInstanceState){
		super.onViewCreated(view, savedInstanceState);
		assignViews(view);
		loadData(mTeleData);
	}

	@Override
	public void setUserVisibleHint(boolean isVisibleToUser) {
		super.setUserVisibleHint(isVisibleToUser);
		if(!viewsAssigned);
		else if(isVisibleToUser)
		{
			assignViews(getView());
			loadData(mTeleData);
			drawPoints();
			
		}
		else if(!isVisibleToUser)
		{
			saveData(mTeleData);
		}
	}
	
	@Override
	public void onPause(){
		super.onPause();
		saveData(mTeleData);
		viewsAssigned=false;
	}
	
	private void loadData(final TeleData teleData){
		intakeTimes = teleData.intakeTimes;
		lowScore.setText(""+teleData.lowScore);
		hotSpots = teleData.hotSpots;
	}
	
	private void saveData(TeleData teleData){
		if(viewsAssigned) {
			teleData.intakeTimes = intakeTimes;
			int lowScoreValue = 0;
			try{
				lowScoreValue = Integer.parseInt(lowScore.getText().toString());
			} catch(NumberFormatException e){
				e.printStackTrace();
				lowScoreValue = 0;
			}
			teleData.lowScore = lowScoreValue;
			teleData.hotSpots = hotSpots;
		}
	}
	
	private void assignViews(View view){
		try{
			buttonUndo = (Button)view.findViewById(R.id.buttonUndo);
			buttonRedo = (Button)view.findViewById(R.id.buttonRedo);
			intakeTime = (TextView)view.findViewById(R.id.titleIntakeTime);
			buttonRecord = (Button)view.findViewById(R.id.buttonRecordIntake);
			buttonLowScoreDown = (Button)view.findViewById(R.id.buttonDownLowScore);
			buttonLowScoreUp = (Button)view.findViewById(R.id.buttonUpLowScore);
			lowScore = (EditText)view.findViewById(R.id.lowScore);
			buttonTruss = (Button)view.findViewById(R.id.buttonTruss);
			buttonCatch = (Button)view.findViewById(R.id.buttonCatch);
			buttonGoal = (Button)view.findViewById(R.id.buttonScore);
			buttonGiveAssist = (Button)view.findViewById(R.id.buttonGiveAssist);
			buttonReceiveAssist = (Button)view.findViewById(R.id.buttonReceiveAssist);
			fieldDiagram = (ImageView)view.findViewById(R.id.fieldDiagram);
						
			if(recording)
				buttonRecord.setText(getResources().getString(R.string.button_recordStop));
			else
				buttonRecord.setText(getResources().getString(R.string.button_recordStart));
			if(intakeTimes.size()>0)
				intakeTime.setText(""+intakeTimes.get(intakeTimes.size()-1));
			
			buttonUndo.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					try{
						backOrder.add(hotSpots.get(hotSpots.size()-1));
						hotSpots.remove(hotSpots.size()-1);	
					} catch(IndexOutOfBoundsException e){
						e.printStackTrace();
					}
					drawPoints();
				}
			});
			
			buttonUndo.setOnLongClickListener(new View.OnLongClickListener() {
					
				@Override
				public boolean onLongClick(View v) {
					try{
						for(int i = hotSpots.size()-1; i > -1; i--){
							backOrder.add(hotSpots.get(i));
							hotSpots.remove(i);
						}
					} catch(IndexOutOfBoundsException e){
						e.printStackTrace();
						return false;
					}
					drawPoints();
					return true;
				}
			});
			
			buttonRedo.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					try{
						hotSpots.add(backOrder.get(backOrder.size()-1));
						backOrder.remove(backOrder.size()-1);
					} catch(IndexOutOfBoundsException e){
						e.printStackTrace();
					}
					drawPoints();
				}
			});
			
			buttonRedo.setOnLongClickListener(new View.OnLongClickListener() {
				
				@Override
				public boolean onLongClick(View v) {
					try{
						for(int i = backOrder.size()-1; i > -1; i--){
							hotSpots.add(backOrder.get(i));
							backOrder.remove(i);
						}
					} catch(IndexOutOfBoundsException e){
						e.printStackTrace();
						return false;
					}
					drawPoints();
					return true;
				}
			});
			
			buttonRecord.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					recording = !recording;
					final Handler handler = new Handler();
					Runnable runnable = new Runnable(){
						@Override
						public void run() {
							while(recording)
							{
								try{
									Thread.sleep(100);
								} catch (InterruptedException e) {
									e.printStackTrace();
								}
								handler.post(new Runnable() {
									@Override
									public void run() {
										double newValue = 0;
										try{
											newValue = Math.floor((Double.parseDouble(intakeTime.getText().toString())+0.10) * 1e2) / 1e2;
										} catch(NumberFormatException e) {
											e.printStackTrace();
											newValue = 0;
										}
										intakeTime.setText(""+newValue);
									}
								});
							}
						}
					};
					
					if(recording) {
						//before starting again, set the time to 0
						intakeTime.setText("0.0");
						
						//update the button text to reflect that it is now a stop button
						buttonRecord.setText(getResources().getString(R.string.button_recordStop));
						new Thread(runnable).start();
					}
					else {
						// update the buton text to reflect that is again a start button
						buttonRecord.setText(getResources().getString(R.string.button_recordStart));
						// update the time in the ArrayList
						double finalTime = 0;
						try{
							finalTime = Math.floor((Double.parseDouble(intakeTime.getText().toString())+0.1) * 1e2) / 1e2;
						} catch(NumberFormatException e){
							e.printStackTrace();
						}
						intakeTimes.add(finalTime);
					}
				}
			});
			
			buttonRecord.setOnLongClickListener(new View.OnLongClickListener() {
				
				@Override
				public boolean onLongClick(View v) {
					try{
						intakeTimes.remove(intakeTimes.size()-1);
					} catch(IndexOutOfBoundsException e){
						e.printStackTrace();
						return false;
					}
					try{
						double newValue = intakeTimes.get(intakeTimes.size()-1);
						intakeTime.setText(""+newValue);
					} catch(IndexOutOfBoundsException e){
						e.printStackTrace();
						intakeTime.setText(getResources().getString(R.string.title_intakeTime));
					}
					return true;
				}
			});
			
			buttonLowScoreDown.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					int newValue = 0;
					try{
						newValue = Integer.parseInt(lowScore.getText().toString())-1;
						if (newValue < 0)
							newValue = 0;
					} catch (NumberFormatException e){
						e.printStackTrace();
						newValue = 0;
					}
					lowScore.setText(""+newValue);
				}
				
			});
			
			buttonLowScoreDown.setOnLongClickListener(new View.OnLongClickListener() {
				
				@Override
				public boolean onLongClick(View v) {
					int newValue = 0;
					lowScore.setText(""+newValue);
					return true;
				}
			});
			
			buttonLowScoreUp.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					int newValue = 0;
					try{
						newValue = Integer.parseInt(lowScore.getText().toString())+1;
					} catch (NumberFormatException e){
						e.printStackTrace();
						newValue = 0;
					}
					lowScore.setText(""+newValue);
				}
				
			});
			
			buttonTruss.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					hSpotType=1;
				}
			});
			
			buttonCatch.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					hSpotType=2;
				}
			});
			
			buttonGoal.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					hSpotType=3;
				}
			});
			
			buttonGiveAssist.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					hSpotType=4;
				}
			});
			
			buttonReceiveAssist.setOnClickListener(new View.OnClickListener() {

				@Override
				public void onClick(View v) {
					hSpotType=5;
				}
			});
			
			fieldDiagram.setOnTouchListener(new View.OnTouchListener(){

				@Override
				public boolean onTouch(View v, MotionEvent event) {
					System.out.println("TOUCH! " + hSpotType);
					switch(event.getAction()){
					case MotionEvent.ACTION_UP:
						PointF point = new PointF(event.getX(),event.getY());
						if(hSpotType!=0){
							double x = point.x / (double)fieldDiagram.getWidth();
							double y=  point.y / (double)fieldDiagram.getHeight();
							HotSpot hotSpot = new HotSpot(hSpotType,x,y);
							hotSpots.add(hotSpot);
							backOrder.clear();
						}
						drawPoints();
					}
					return true;
				}
				
			});
			viewsAssigned=true;
		} catch (Exception e){
			e.printStackTrace();
			viewsAssigned=false;
		}
	}
	
	public boolean onMyKeyDown(int keyCode){
		switch(keyCode){
		case KeyEvent.KEYCODE_BUTTON_A:
			buttonRecord.performClick();
			break;
		case KeyEvent.KEYCODE_BUTTON_Y:
			buttonRecord.performLongClick();
			break;
		case KeyEvent.KEYCODE_BUTTON_B:
			buttonLowScoreUp.performClick();
			break;
		case KeyEvent.KEYCODE_BUTTON_X:
			buttonLowScoreDown.performClick();
			break;
		case KeyEvent.KEYCODE_BUTTON_THUMBL:
			buttonUndo.performClick();
			break;
		case KeyEvent.KEYCODE_BUTTON_THUMBR:
			buttonRedo.performClick();
			break;
		default:
			break;
		}
		return true;
	}
	
	private void drawPoints(){
		Bitmap background = BitmapFactory.decodeResource(getResources(), R.drawable.field_layout_tele);
		Bitmap bmp = Bitmap.createScaledBitmap(background, fieldDiagram.getWidth(),fieldDiagram.getHeight(),true);
		Canvas canvas = new Canvas(bmp);
		
		Paint paint = new Paint();
		paint.setStyle(Style.FILL);
		for(HotSpot h : hotSpots){
			int color = getResources().getColor(R.color.Transparent);
			String text = "";
			switch(h.type){
			case 1:
				color = getResources().getColor(R.color.Blue);
				text = "T";
				break;
			case 2:
				color = getResources().getColor(R.color.Red);
				text = "C";
				break;
			case 3:
				color = getResources().getColor(R.color.Green);
				text = "G";
				break;
			case 4:
				color = getResources().getColor(R.color.Pink);
				text = "GA";
				break;
			case 5:
				color = getResources().getColor(R.color.Purple);
				text = "RA";
				break;
			default:
				color = getResources().getColor(R.color.Black);
				text = "";
				break;
			}
			paint.setColor(color);
			float x = (float) ((float)fieldDiagram.getWidth()*h.x);
			float y = (float) ((float)fieldDiagram.getHeight()*h.y);
			canvas.drawCircle(x, y, 10, paint);
			canvas.drawText(text, x-15, y-10, paint);
		}
		fieldDiagram.setImageBitmap(bmp);
	}
	
}