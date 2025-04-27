package com.api;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.KeyPair;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.util.List;

public class SocketServer {
    private static final int PORT = 12345;
    private static KeyPair keyPair;

    public static void main(String[] args) throws Exception {
        keyPair = RSAUtils.generateKeyPair();
        System.out.println(keyPair.getPublic().toString());
        ServerSocket serverSocket = new ServerSocket(PORT);
        System.out.println("Server sulla porta " + PORT);

        while (true) {
            Socket clientSocket = serverSocket.accept();
            System.out.println("Connessione accettata da: " + clientSocket.getInetAddress());
            new Thread(new ClientHandler(clientSocket, keyPair.getPrivate(), keyPair.getPublic())).start();
        }
    }

    public static void handleMessage(String message, PrintWriter writer, PrivateKey privateKey) {
        System.out.println("Messaggio ricevuto e decifrato: " + message);
        if (message.contains("on")) {
            try {
                WakeOnLan.wakeOnLan(message);
                writer.println("on");
            } catch (Exception e) {
                writer.println("err");
            }

        }
        if (message.contains("scan")) {
            try {
                List<Device> devices = NetworkScanner.scanNetwork("192.168.1");
                System.out.println("Dispositivi trovati:");
                for (Device d : devices) {
                    writer.println(d.ip + " " + d.hostname);
                    System.out.println(d);
                }
                
            } catch (Exception e) {
                writer.println("err");
            }
        }
    }

    private static class ClientHandler implements Runnable {
        private Socket socket;
        private PrivateKey privateKey;
        private PublicKey publicKey;

        public ClientHandler(Socket socket, PrivateKey privateKey, PublicKey publicKey) {
            this.socket = socket;
            this.privateKey = privateKey;
            this.publicKey = publicKey;
        }

        @Override
        public void run() {
            try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
                OutputStream os = socket.getOutputStream();
                PrintWriter writer = new PrintWriter(os, true);
                String encryptedMessage = in.readLine();
                if (encryptedMessage.contains("publicKey")) {
                    writer.println(publicKey);
                } 
                if (encryptedMessage.contains("close")) {
                    writer.println("ok");
                }else {
                    if (encryptedMessage != null) {
                        String decryptedMessage = RSAUtils.decrypt(encryptedMessage, privateKey);
                        handleMessage(decryptedMessage, writer, privateKey);
                    }
                }

            } catch (Exception e) {
                
                System.err.println("Errore nella gestione del client: " + e.getMessage());
            } finally {
                try {
                    socket.close();
                } catch (IOException ignored) {
                }
            }
        }
    }
}
