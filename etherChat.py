import threading
import struct
from scapy.all import *

CUSTOM_ETHERTYPE = 0x88B5
INTERFACE = "VirtualBox Host-Only Ethernet Adapter"
DEST_MAC = "08:00:27:2c:9f:1a" 

def receive_thread():
    # Keep this inside the thread so it has the right scope
    MY_MAC = get_if_hwaddr(INTERFACE) 
    
    def process_packet(packet):
        # Good call on the .lower() comparison!
        if Ether in packet and packet[Ether].src.lower() == MY_MAC.lower():
            return

        if packet.haslayer(Raw):
            raw_data = bytes(packet[Raw].load)
            if len(raw_data) >= 4:
                msg_len = struct.unpack("!I", raw_data[:4])[0]
                message = raw_data[4:4+msg_len].decode('utf-8', errors='ignore')
                
                # FIX: \033[K is an escape code that clears the line to the right.
                # This fixes the "You: You:" mess from image_bc6e82.png
                print(f"\rPartner: {message}\033[K\nYou: ", end="", flush=True)

    # Indent this so it's inside receive_thread!
    sniff(iface=INTERFACE, filter="ether proto 0x88B5", prn=process_packet, store=False)

def main():
    listener = threading.Thread(target=receive_thread, daemon=True)
    listener.start()

    print(f"Chat started on {INTERFACE}. Get to typing!")
    
    while True:
        try:
            msg = input("You: ")
            if not msg: continue
            
            payload = struct.pack("!I", len(msg)) + msg.encode()
            # Explicitly setting src is great for troubleshooting
            frame = Ether(src=get_if_hwaddr(INTERFACE), dst=DEST_MAC, type=CUSTOM_ETHERTYPE) / Raw(load=payload)
            
            sendp(frame, iface=INTERFACE, verbose=False)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()