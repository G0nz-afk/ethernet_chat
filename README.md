# ethernet_chat
Who needs IP addresses? A raw Layer 2 chat application built with Scapy and Python for direct Ethernet frame communication between local network nodes. 

EtherChat is a Python-based chat application that demonstrates direct communication between two systems using raw Ethernet frames. By operating at the Data Link Layer (Layer 2) of the OSI model, this tool bypasses the traditional IPv4/IPv6 networking stack entirely.

Features:
-No IP Required: Communicates using MAC addresses and a custom EtherType (0x88B5).
-Custom Protocol: Implements a lightweight message format with a 4-byte length header.
-Echo Suppression: Automatically filters out local loopback frames to ensure a clean chat UI.
-Graceful Handling: Integrated support for keyboard interrupts and real-time console refreshing.

How it works:
Most modern applications use the standard networking stack (Link -> Internet -> Transport -> Application). EtherChat "jumps" directly from the Link layer to the Application layer.

Message Format:
-Each frame contains a custom payload structure:
  1. Header (4 bytes): An unsigned integer (Big-endian) representing the length of the message.
  2. Payload (Variable): The UTF-8 encoded string message.

Prerequisites:
-Python 3.x
-Scapy: Install via pip install scapy
-Npcap (Windows) or libpcap (Linux): Required for raw packet injection and sniffing.
-Administrative Privileges: Raw sockets require sudo or Administrator access to run.

Configuration:
Before running, open etherChat.py and update the INTERFACE and DEST_MAC variables.
On Windows, use ipconfig /all to find your adapter name.
On Linux, use ip link to find your interface
-INTERFACE: The name of your network adapter 
-DEST_MAC: The hardware MAC address of the partner machine.

Usage:
-On Machine A (Receiver/Sender):
-Bash
  # Linux
  sudo python3 etherChat.py
  # Windows (Run PowerShell as Admin)
  python etherChat.py
  On Machine B (Partner):
  Repeat the same command.
-Chat: Type your message and hit Enter. The incoming messages will appear labeled as Partner.

Security Note
-This project is for educational purposes. Because it operates at Layer 2, it is not routable across the internet. It is intended for use in controlled, local environments or virtualized networks (like VirtualBox).

<img width="651" height="441" alt="Screenshot 2026-05-14 022205" src="https://github.com/user-attachments/assets/6ea3e56a-0596-4bde-9d3c-f3973ca745f3" />
