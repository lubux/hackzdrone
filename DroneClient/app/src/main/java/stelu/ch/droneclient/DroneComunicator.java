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

    public static final String IP_BASIC = "172.31.3.23";
    public static final int PORT_DRONE = 8080;

    public static final int MSG_ID_LOCATION = 1;

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

    @Override
    public void close() throws IOException {
        socket.close();
    }
}