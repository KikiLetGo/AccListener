# AccListener
这是一个基于2020年2月份浙江大学发布的论文而实现的安卓加速度传感器监听程序(项目中有从arxiv.org下载的论文)。
出于安全考虑，数据集暂时不能提供，但是思路很简单，preworks文件夹里有一个录音的脚本，大家自己录制就好了。然后放在安卓工程里自动播放和手机加速度传感器的数据。

安卓的录音采集加速度数据的代码很简单，我全部写在了一个activity中了，就不单独发布项目了，直接把代码在这里贴出来
```java
====MainActivity.java=====
package com.elexlab.acclistener;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventCallback;
import android.hardware.SensorEventListener;
import android.hardware.SensorListener;
import android.hardware.SensorManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;

import com.elexlab.acclistener.pojo.Vec3;
import com.elexlab.acclistener.view.ChartView;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Queue;

public class MainActivity extends AppCompatActivity {

    Vec3 vec;
    int count = 0;
    private boolean isPlaying = false;
    private List<Vec3> accDatas = new ArrayList<>();
    private void requestPermissions() {
        // 如果未获得外部存储读写权限，则申请
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            // 申请权限
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
        }
    }
    private  MediaPlayer mediaPlayer;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        requestPermissions();
        mediaPlayer = new MediaPlayer();

        final ChartView cvChart = findViewById(R.id.cvChart);
        final Queue<Double> queue = new ArrayDeque();
        SensorManager mSensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        Sensor sensor = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        boolean result = mSensorManager.registerListener(new SensorEventListener() {
            @Override
            public void onSensorChanged(SensorEvent sensorEvent) {
                if(isPlaying&&accDatas!=null) {

                    if (vec == null) {
                        vec = new Vec3(sensorEvent.values);
                    }
                    Vec3 vec3 = new Vec3(sensorEvent.values);
                    if (queue.size() >= 500) {
                        queue.poll();
                    }
                    queue.offer(vec3.distance(vec) * 2);
                    cvChart.resetValues(queue);
                    accDatas.add(vec3);
                }
            }
            @Override
            public void onAccuracyChanged(Sensor sensor, int i) {

            }
        }, sensor, SensorManager.SENSOR_DELAY_FASTEST);
        Log.d("MainActivity","result:"+result);
        loopPlayAudiosAndRecord();
    }

    private int currentPlayIndex = 0;

    private void loopPlayAudiosAndRecord(){
        final String dirPath= Environment.getExternalStoragePublicDirectory("Download").getPath()+"/AccListener/data/sleep/";
        File dir = new File(dirPath);
        final File[] files = dir.listFiles();
        String fullFilePath = dirPath+files[currentPlayIndex].getName();
        Log.d("Acc","fullFilePath:"+fullFilePath);
        playAudio(fullFilePath, new MediaPlayer.OnCompletionListener() {
            @Override
            public void onCompletion(MediaPlayer mediaPlayer) {
                Log.d("Acc:","play end");
                oneRecordEnd();
                currentPlayIndex ++;
                if(currentPlayIndex>=files.length){
                    saveResult();
                    return;
                }
                String fileName;
                while(!(fileName = files[currentPlayIndex].getName()).endsWith("wav")){
                }
                String fullFilePath = dirPath + fileName;
                if(!fullFilePath.endsWith("wav")){

                }
                Log.d("Acc","fullFilePath:"+fullFilePath);
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                playAudio(fullFilePath,this);
            }
        });


    }
    private void saveResult(){
        final String dirPath= Environment.getExternalStoragePublicDirectory("Download").getPath()+"/AccListener/data";
        try {
            FileWriter fileOutputStream = new FileWriter(new File(dirPath+"sleep.txt"));
            fileOutputStream.write(resultsData.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void oneRecordEnd(){
        isPlaying = false;
        if(accDatas != null){
            Log.d("Acc:","accDatas size:"+accDatas.size());
            resultsData.append(accDatas.toString());
            resultsData.append("\n");

            accDatas.clear();
        }
    }

    StringBuffer resultsData = new StringBuffer();
    private void playAudio(final String filePath,MediaPlayer.OnCompletionListener onCompletionListener){
        mediaPlayer.reset();
        mediaPlayer.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
            @Override
            public void onPrepared(MediaPlayer mediaPlayer) {
                Log.d("Acc:","playing:"+filePath);
                mediaPlayer.start();
                isPlaying = true;
            }
        });
        try {
            mediaPlayer.setDataSource(filePath);
            mediaPlayer.prepare();
        } catch (IOException e) {
            e.printStackTrace();
        }


        mediaPlayer.setOnCompletionListener(onCompletionListener);
    }
}
====Vec3.java===
package com.elexlab.acclistener.pojo;

import android.util.Log;

import androidx.annotation.NonNull;

public class Vec3 {
    private float x;
    private float y;
    private float z;

    public Vec3(float x, float y, float z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public Vec3(float[] array) {
        this.x = array[0];
        this.y = array[1];
        this.z = array[2];
    }

    public float getX() {
        return x;
    }

    public void setX(float x) {
        this.x = x;
    }

    public float getY() {
        return y;
    }

    public void setY(float y) {
        this.y = y;
    }

    public float getZ() {
        return z;
    }

    public void setZ(float z) {
        this.z = z;
    }
    public double distance(Vec3 vec3){
        double dis = Math.sqrt(Math.pow(vec3.x-this.x,2)+Math.pow(vec3.y-this.y,2)+Math.pow(vec3.z-this.z,2));
        return dis;
    }

    @NonNull
    @Override
    public String toString() {
        return "["+x+","+y+","+z+"]";

    }

}

===ChartView.java====
package com.elexlab.acclistener.view;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.View;

import androidx.annotation.Nullable;

import java.util.Collection;
import java.util.List;

public class ChartView extends View {
    public ChartView(Context context) {
        super(context);
    }

    public ChartView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
    }

    public ChartView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }

    public ChartView(Context context, @Nullable AttributeSet attrs, int defStyleAttr, int defStyleRes) {
        super(context, attrs, defStyleAttr, defStyleRes);
    }

    private Collection<Double> values;
    public void resetValues(Collection<Double> values){
        this.values = values;
        invalidate();
    }

    Paint paint;
    float scale = 1000;
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if(paint == null){
            paint=new Paint();//新建画笔
            paint.setAntiAlias(true);//设置抗锯齿
            paint.setStyle(Paint.Style.STROKE);//实心
            paint.setStrokeWidth(2);//线条粗细
        }

        canvas.drawColor(Color.WHITE);
        if(values == null || values.size() <= 0){
            return;
        }
        float startX=0;
        float startY=0;
        float endX=0;
        float endY=0;
        int time=0;
        for(Double value:values){
            endX = time;
            endY = value.floatValue()*scale;

            canvas.drawLine(startX,startY,endX,endY,paint);

            time +=2;
            startX = endX;
            startY = endY;
        }
    }
}

```
