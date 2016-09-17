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
import android.view.View;

import java.io.IOException;
import java.net.SocketException;

public class MainActivity extends AppCompatActivity {

    private LocationManager locationManager = null;
    private GPSListener listener = null;
    private DroneComunicator drone_com;

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
    }

    public void onClickSendLoc(View v) {
        startSendingLocation();
    }

    public void onStopSendLoc(View v) {
        stoptSendingLocation();
    }

    public void onQRCode(View v) {
        Intent intent = new Intent(this, qrcodeactivity.class);
        startActivity(intent);
    }

    public void startSendingLocation() {
        listener = new GPSListener(drone_com);

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
        locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0, 0, listener);
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
        locationManager.removeUpdates(listener);
    }

    public static class GPSListener implements LocationListener {

        private DroneComunicator comunicator;
        private static long MIN_WAIT_TIME = 2000;

        private long curtime = -1;

        public GPSListener(DroneComunicator comunicator) {
            this.comunicator = comunicator;
        }

        @Override
        public void onLocationChanged(Location location) {
            long ms = System.currentTimeMillis();
            try {
                if(curtime==-1 || (curtime - ms > MIN_WAIT_TIME)) {
                    comunicator.sendLocation(location);
                    curtime = ms;
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
