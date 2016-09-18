package stelu.ch.droneclient;

import android.graphics.Bitmap;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.WriterException;
import com.google.zxing.common.BitMatrix;
import com.google.zxing.qrcode.QRCodeWriter;

import java.io.IOException;

public class QRCodeActivity extends AppCompatActivity {

    private ImageView imgView;
    private Button button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_qrcode2);
        imgView = (ImageView)findViewById(R.id.imageView);
        imgView.setImageBitmap(loadQRCode("Banana!!"));
        button = (Button) findViewById(R.id.button2);
        //button.setVisibility(View.INVISIBLE);
        (new CodeChecker()).execute();

    }

    private Bitmap loadQRCode(String code) {
        QRCodeWriter writer = new QRCodeWriter();
        try {
            BitMatrix bitMatrix = writer.encode(code, BarcodeFormat.QR_CODE, 512, 512);
            int width = bitMatrix.getWidth();
            int height = bitMatrix.getHeight();
            Bitmap bmp = Bitmap.createBitmap(width, height, Bitmap.Config.RGB_565);
            for (int x = 0; x < width; x++) {
                for (int y = 0; y < height; y++) {
                    bmp.setPixel(x, y, bitMatrix.get(x, y) ? Color.BLACK : Color.WHITE);
                }
            }
            return bmp;
        } catch (WriterException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void onRetry(View v) {
        finish();
    }

    public class CodeChecker extends AsyncTask<Void, Void, Boolean> {
        @Override
        protected Boolean doInBackground(Void... params) {
            try {
                return MainActivity.drone_com.scanOK();
            } catch (IOException e) {
                return false;
            }

        }

        @Override
        protected void onPostExecute(Boolean aBoolean) {
            super.onPostExecute(aBoolean);
            if(aBoolean) {
                imgView.setVisibility(View.INVISIBLE);
                button.setVisibility(View.VISIBLE);
                button.setText("SCAN OK ORDER AGAIN");
            } else {
                imgView.setVisibility(View.INVISIBLE);
                button.setVisibility(View.VISIBLE);
                button.setText("WRONG ORDER!!");
            }
        }
    }
}
