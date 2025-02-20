trying to figure out why the udp scanning is so slow 
there is a send delay which is used to prevent nmap from flooding the network with packets?
udp scans are naturally slow because unlike tcp, there is no established handshake between a client and a server. when we conduct a tcp scan, we send out a SYN handshake, and if the port is closed, then we receive the RST packet letting us know that the port is closed. However, when it comes to UDP scanning, packets can be dropped without relaying information back to the sender. This means that unless the sender knows the service running on a particular port, or the specific format of packets to send, it's hard in a UDP scan to detect if a port is open or not. 


right this was the openradius crap that we had to do 

TODO:
- [ ] Figure out how to expedite the UDP scan 
    -> https://nmap.org/book/scan-methods-udp-scan.html#scan-methods-udp-optimizing
    -> some nmap documentation talking about this  
    -> nmap -vvv -sU -sV --min-hostgroup 100 -F --host-timeout 5s $HTBHOST

http://underpass.htb/daloradius/app/users/login.php
i think i was trying some default credentials for this, but it's not admin but this is 
http://underpass.htb/daloradius/app/operators


so maybe we do an ssh tunnel into the ssh connection

underwaterfriends


