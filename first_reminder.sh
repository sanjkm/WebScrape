#!/bin/bash
cd /home/smenon/Web
if [ -s Tory.txt ]
then
	cat send_email_template.txt Tory.txt | msmtp --from=default -t sanjay.menon@gmail.com
fi
