package stelu.ch.droneclient;

import android.location.Location;
import android.os.AsyncTask;
import android.util.Log;

import java.io.Closeable;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;

/**
 * Created by lukas on 17.09.16.
 */
public class DroneComunicator implements Closeable {

    public static final String IP_BASIC = "255.255.255.255";
    public static final int PORT_DRONE = 8080;

    public static final int MSG_ID_LOCATION = 1;
    public static final int MSG_ID_STOP = 2;
    public static final int MSG_OK = 3;
    public static final int MSG_ERR = 4;

    private DatagramSocket socket;
    private InetAddress addr = null;

    public DroneComunicator(String ip, int port) throws SocketException {
        socket = new DatagramSocket(port);
        try {
            addr = InetAddress.getByName(ip);
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
    }

    public DroneComunicator() throws SocketException {
        socket = new DatagramSocket(PORT_DRONE);
        try {
            addr = InetAddress.getByName(IP_BASIC);
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
    }

    public void sendLocation(Location location) throws IOException {
        byte[] buffer = new byte[17];
        ByteBuffer buff = ByteBuffer.wrap(buffer);
        buff.put((byte) MSG_ID_LOCATION);
        buff.putDouble(location.getLatitude());
        buff.putDouble(location.getLongitude());
        Log.i("INFO", String.valueOf(location.getLatitude()) + " " + String.valueOf(location.getLongitude()));
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length, addr, PORT_DRONE);
        (new AsyncTask<DatagramPacket, Void, String>(){
            @Override
            protected String doInBackground(DatagramPacket... params) {
                try {
                    socket.send(params[0]);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                return null;
            }
        }).execute(packet);

    }

    public void stopDrone() {
        byte[] buffer = new byte[1];
        buffer[0] = MSG_ID_STOP;
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length, addr, PORT_DRONE);
        (new AsyncTask<DatagramPacket, Void, String>(){
            @Override
            protected String doInBackground(DatagramPacket... params) {
                try {
                    socket.send(params[0]);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                return null;
            }
        }).execute(packet);
    }

    public boolean scanOK() throws IOException {
        while (true) {
            byte[] buffer = new byte[1];
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length, addr, PORT_DRONE);
            socket.receive(packet);
            if (packet.getData()[0] == MSG_OK) {
                return true;
            } else if (packet.getData()[0] == MSG_ERR){
                return false;
            }
        }
    }

    @Override
    public void close() throws IOException {
        socket.close();
    }
}
