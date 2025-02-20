git-dumper to get all the git files

not sure what this is first of all ghost?

this looks like an out of date version me thinks 


COPY wait-for-it.sh /var/lib/ghost/wait-for-it.sh
COPY entry.sh /entry.sh
RUN chmod +x /var/lib/ghost/wait-for-it.sh
RUN chmod +x /entry.sh

ENTRYPOINT ["/entry.sh"]
CMD ["node", "current/index.js"]

there is also a wait-for-it.sh script somewhere but it doesnt seem like it's in the git repo


arbitrary file read but we need a username / password
https://github.com/0xDTC/Ghost-5.58-Arbitrary-File-Read-CVE-2023-40028

potential admin usernames
sam
djordje
neovim is highlighting something in red and it points us to a authentication.test.js file, but not sure what the red dot is and i feel like i should know because it is very much so a needle in the haystack thing 

└─$ git status          
Not currently on any branch.
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   ../../../../../../Dockerfile.ghost
        modified:   authentication.test.js

 shows uncommitted changes so these were changes which haven't been pushed just yet?

linkvortex.htb/ghost/#/signin

sam@ghost.org
zimo@ghost.org
admin+1@ghost.org

thisissupersafe
OctopiFociPilfer45


what is the username / email to use and where to find it?

there is dev@linkvortex.htb in .git/logs/HEAD?
i guess you have to guess that the admin email is admin@linkvortex.htb?
./CVE-2023-40028 -u 'admin@linkvortex.htb' -p 'OctopiFociPilfer45' -h htt
p://linkvortex.htb

had to edit a little bit of the script
if permissions error -> throw 500 error


reading production.json file
/var/lib/ghost/config.production.json
"user": "bob@linkvortex.htb",
"pass": "fibber-talented-worth"


once again, not sure what to look for in the priv esc
the /opt/ghost/content directory looks like it just has some javascript code, but nothing that gives a hint about priv esc 

there might not be laurel anywhere unfortunately
forgot about sudo -l 
weird that we have a sudo file but it can't be executed?
never seen this before really 
never mind just need to use sudo keyword
we can read specific files, but not root or etc files 
