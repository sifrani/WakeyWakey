package com.api;

import java.io.PrintWriter;
import java.net.Socket;
import java.security.KeyPair;
import java.security.PublicKey;

public class SocketClient {
    public static void main(String[] args) throws Exception {
        String serverAddress = "localhost";
        int port = 12345;

        // Simuliamo la chiave pubblica del server (normalmente la ricevi o la conosci)
        KeyPair keyPair = RSAUtils.generateKeyPair(); // SOLO PER TEST — in realtà riceveresti la public key dal server
        PublicKey publicKey = keyPair.getPublic();

        // Test message da cifrare
        String message = "Ciao server, sono un client!";

        // Cifra il messaggio
        String encrypted = RSAUtils.encrypt(message, publicKey);

        // Connessione al server
        Socket socket = new Socket(serverAddress, port);
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
        out.println(encrypted);
        socket.close();

        System.out.println("Messaggio cifrato inviato al server!");
    }
}