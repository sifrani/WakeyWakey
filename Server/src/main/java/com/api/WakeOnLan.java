package com.api;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class WakeOnLan {

    public static void wakeOnLan(String macAddress) throws Exception {
        // IP broadcast della rete locale (modifica se necessario)
        String broadcastIP = "255.255.255.255"; 
        int port = 9; // Porta standard per WOL

        byte[] macBytes = getMacBytes(macAddress);
        byte[] packetData = new byte[6 + 16 * macBytes.length];

        // I primi 6 byte devono essere 0xFF
        for (int i = 0; i < 6; i++) {
            packetData[i] = (byte) 0xFF;
        }

        // Ripeti il MAC 16 volte
        for (int i = 6; i < packetData.length; i += macBytes.length) {
            System.arraycopy(macBytes, 0, packetData, i, macBytes.length);
        }

        InetAddress address = InetAddress.getByName(broadcastIP);
        DatagramPacket packet = new DatagramPacket(packetData, packetData.length, address, port);
        DatagramSocket socket = new DatagramSocket();
        socket.setBroadcast(true);
        socket.send(packet);
        socket.close();

        System.out.println("Pacchetto WOL inviato a " + macAddress);
    }

    private static byte[] getMacBytes(String macStr) throws IllegalArgumentException {
        byte[] bytes = new byte[6];
        String[] hex = macStr.split("[:\\-]");
        if (hex.length != 6) {
            throw new IllegalArgumentException("MAC address non valido.");
        }
        for (int i = 0; i < 6; i++) {
            bytes[i] = (byte) Integer.parseInt(hex[i], 16);
        }
        return bytes;
    }

    public static void main(String[] args) {
        try {
            // Inserisci il tuo MAC address qui
            wakeOnLan("00:11:22:33:44:55");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
