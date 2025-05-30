#!/bin/sh
# In order to check Tellicast process
# and if the license is ok:
# host_key_4 = ****-****-****-**** (Aladdin EToken PRO)


# In order to keep only the last three days on the log
LOGFILE="/var/www/html/SHOWCast.GR/Logs/check-tellicast.log"
NEWLOGFILE="/var/www/html/SHOWCast.GR/Logs/check-tellicast.tmp"
touch $NEWLOGFILE

NDAYS=5 #Number of days ago to preserve

DATE=`date +"%Y-%m-%d %T %Z"`
FROMDATE=`date +"%Y-%m-%d" -d "$NDAYS day ago"`
#echo $FROMDATE

# Get the lines from the 1st occurance of FROMDATE until last line
/usr/bin/sed -n "/^${FROMDATE}/,/tail -n 1/p" $LOGFILE > $NEWLOGFILE

# Replase the log file with the tailored one
if [ -s $NEWLOGFILE ]
then
    #echo "Replacing Log File"
    mv $NEWLOGFILE $LOGFILE
else
    echo "$NEWLOGFILE is empty"
    rm $NEWLOGFILE
fi

# Create the timestamp at the Log file
echo $DATE >> $LOGFILE

ip=`/sbin/ifconfig  | grep 'inet '| grep -v '127.0.0.1' | grep -v '192'| cut -d: -f2 | awk '{ print $2}'`

# Check if Tellicast Service is running
SERVICE="tc-cast-client"
if pgrep -x "$SERVICE" >/dev/null
then
    echo "$SERVICE is running" >> $LOGFILE
    # Check if license is ok
    # giving a specific amount of time (timeout) so to avoid hanging
    LASTKEY="$(timeout 5s /usr/local/bin/tc-cast-client -k 2>&1 | tail -1 )" 
   #  LASTKEY="$(/usr/local/bin/tc-cast-client -k 2>&1 | tail -1 )"
    if [ "${LASTKEY:0:10}" = "host_key_4" ]; then
	echo " with: " $LASTKEY >> $LOGFILE
    else
	echo "     ... but without license, $LASTKEY" >> $LOGFILE
	echo "Try to fix it by restarting $SERVICE" >> $LOGFILE
	systemctl restart tellicast-client.service
	# After restarting service check if license is ok, again
	LASTKEY="$(timeout 5s /usr/local/bin/tc-cast-client -k 2>&1 | tail -1 )"
	if [ "${LASTKEY:0:10}" = "host_key_4" ]; then
	   echo "Ok, Fixed it: " $LASTKEY >> $LOGFILE
	else
	   echo "Nada :( ...Send email to report it" >> $LOGFILE
	   # Send mail to inform that a reboot might is need it
	   /usr/sbin/sendmail "omety.pmkata@hnms.gr"<<-EOF
		Subject: Tellicast License @ $HOSTNAME
		!!! Warning !!!
		$DATE Tellicast Service at $HOSTNAME with IP $ip cannot read the license
		EOF
	fi
    fi
else
    echo "$SERVICE stopped" >> $LOGFILE
    # uncomment to start service if stopped
    systemctl start tellicast-client.service
    # Check if the servie is started
    if pgrep -x "$SERVICE" >/dev/null
    then
	echo "Ok. $SERVICE started" >> $LOGFILE
    else
    	# mail 
    	/usr/sbin/sendmail "omety.pmkata@hnms.gr"<<-EOF
		Subject: Tellicast Service @ $HOSTNAME
		!!! Warning !!!
		$DATE Tellicast Service at $HOSTNAME with IP $ip is NOT running
	EOF
    fi
fi
