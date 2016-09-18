package stelu.ch.droneclient;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.io.IOException;
import java.net.SocketException;
import java.util.concurrent.atomic.AtomicBoolean;

public class MainActivity extends AppCompatActivity {

    private LocationManager locationManager = null;
    private GPSListener listener = null;
    public static DroneComunicator drone_com;
    private boolean buttonIsStart = true;

    private ProgressBar bar;
    private TextView loadingText;
    private  ImageView imgv;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        locationManager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);
        try {
            drone_com = new DroneComunicator();
        } catch (SocketException e) {
            e.printStackTrace();
        }
        listener = new GPSListener(drone_com);
        imgv = (ImageView) findViewById(R.id.imageView2);
        imgv.setImageResource(R.drawable.large);

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        // locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0, 0, listener);
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, listener);
        bar = (ProgressBar) findViewById(R.id.progressBar);
        loadingText = (TextView) findViewById(R.id.driving);
        bar.setVisibility(View.INVISIBLE);
        loadingText.setVisibility(View.INVISIBLE);
    }

    @Override
    protected void onStop() {
        super.onStop();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        locationManager.removeUpdates(listener);
        try {
            this.drone_com.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void onClickSendLoc(View v) {
        Button button = (Button) v;
        if (buttonIsStart) {
            buttonIsStart = false;
            startSendingLocation();
            button.setText("Drone is near");
            this.loadingText.setVisibility(View.VISIBLE);
            this.bar.setVisibility(View.VISIBLE);
            this.imgv.setVisibility(View.INVISIBLE);

        } else {
            buttonIsStart = true;
            stoptSendingLocation();
            button.setText("Order Banana");
            this.loadingText.setVisibility(View.INVISIBLE);
            this.bar.setVisibility(View.INVISIBLE);
            this.imgv.setVisibility(View.VISIBLE);
            Intent intent = new Intent(this, QRCodeActivity.class);
            startActivity(intent);
        }

    }

    public void onQRCode(View v) {
        Intent intent = new Intent(this, QRCodeActivity.class);
        startActivity(intent);
    }

    public void startSendingLocation() {
        listener.setSendable();
        if(listener.getLocation()!=null) {
            try {
                drone_com.sendLocation(listener.getLocation());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

    }

    public void stoptSendingLocation() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        this.listener.setPassive();
        drone_com.stopDrone();
    }

    public static class GPSListener implements LocationListener {

        private DroneComunicator comunicator;
        private static long MIN_WAIT_TIME = 2000;
        private Location lastLocation = null;
        private AtomicBoolean inSendMode = new AtomicBoolean(false);

        private long curtime = -1;

        public GPSListener(DroneComunicator comunicator) {
            this.comunicator = comunicator;
        }

        public Location getLocation() {
            return lastLocation;
        }

        public void setSendable() {
            this.inSendMode.set(true);
        }

        public void setPassive() {
            this.inSendMode.set(false);
        }

        @Override
        public void onLocationChanged(Location location) {
            long ms = System.currentTimeMillis();
            Log.i("INFO", "loc changed");
            try {
                if(curtime==-1 || (curtime - ms > MIN_WAIT_TIME)) {
                    if(inSendMode.get())
                        comunicator.sendLocation(location);
                    curtime = ms;
                    this.lastLocation = location;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {

        }

        @Override
        public void onProviderEnabled(String provider) {

        }

        @Override
        public void onProviderDisabled(String provider) {

        }
    }
}
