package com.api;

public class Device {
    public String ip;
    public String hostname;

    public Device(String ip, String hostname) {
        this.ip = ip;
        this.hostname = hostname;
    }

    @Override
    public String toString() {
        return ip + " (" + hostname + ")";
    }
}
