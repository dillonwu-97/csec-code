from scapy.all import *
from base64 import b64decode

def main():
    packets = rdpcap('./semaphore.pcap')

    c = b''
    for p in packets:
        raw_data = bytes(p)
        c += raw_data[0x2f].to_bytes(1, 'little')
    print(b64decode(c.decode()))
    # flag: USCG{s3map4h0r3_tcp_f1ag5}

if __name__ == '__main__':
    main()
