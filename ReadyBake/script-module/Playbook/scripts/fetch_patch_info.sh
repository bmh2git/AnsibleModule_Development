#!/bin/sh
if [ -f /var/log/dpkg.log ]
then
	cat /var/log/dpkg.log
else
	echo "No patching log file found."
fi
