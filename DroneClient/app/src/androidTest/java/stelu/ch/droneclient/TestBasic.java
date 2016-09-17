package stelu.ch.droneclient;

import android.test.InstrumentationTestCase;

import java.nio.ByteBuffer;

/**
 * Created by lukas on 17.09.16.
 */
public class TestBasic extends InstrumentationTestCase {

    public void testEnpack() throws Exception {
        byte[] buffer = new byte[17];
        double a=0.2, b = 0.3;
        ByteBuffer buff = ByteBuffer.wrap(buffer);
        buff.put((byte) 1);
        buff.putDouble(a);
        buff.putDouble(b);
    }

}
