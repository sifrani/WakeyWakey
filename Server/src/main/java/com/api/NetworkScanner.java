package com.api;

import java.io.IOException;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class NetworkScanner {

    public static List<Device> scanNetwork(String subnet) {
        List<Device> foundDevices = Collections.synchronizedList(new ArrayList<>());
        ExecutorService executor = Executors.newFixedThreadPool(50);

        for (int i = 1; i < 255; i++) {
            String host = subnet + "." + i;
            executor.execute(() -> {
                try {
                    InetAddress address = InetAddress.getByName(host);
                    if (address.isReachable(100)) {
                        foundDevices.add(new Device(host, address.getHostName()));
                    }
                } catch (IOException ignored) {}
            });
        }

        executor.shutdown();
        while (!executor.isTerminated()) {
            try {
                Thread.sleep(10);
            } catch (InterruptedException ignored) {}
        }

        return foundDevices;
    }

    public static void main(String[] args) {
        List<Device> devices = scanNetwork("192.168.1");
        System.out.println("Dispositivi trovati:");
        for (Device d : devices) {
            System.out.println(d);
        }
    }
}

