#!/bin/bash

# Define variables
SSHCMD="ssh -l user" # Sustitiute for your user
MYMACHINES="server1 sever2" # Enter your servers
LOG_DIR="/tmp"
LOG_FILES=""
SenderEmail="do-not-reply@example.com"
ReportToEmail="itst@example.com"


# Loop through each machine in MYMACHINES
for thismachine in $MYMACHINES ; do

    # Define the log file for this machine
    log_file="$LOG_DIR/$thismachine.log"

    # Run commands on remote machine and save output to log file
    pending_updates=$($SSHCMD $thismachine -C "apt list --upgradable 2>/dev/null | grep -c 'upgradable'")

    # Save the number of updates to log file
    {
        echo ""
        echo "=============================================================="
        echo "                   Checking $thismachine                     "
        echo "=============================================================="
        echo ""
        echo "Static hostname: $thismachine"
        $SSHCMD $thismachine -C "hostnamectl | grep 'System\|Kernel'"
        echo ""
        $SSHCMD $thismachine -C "uptime"
        echo ""
        echo "Pending updates: $pending_updates"
        echo ""
    } > "$log_file"

    # Add this log file to the list of files to be emailed
    LOG_FILES="$LOG_FILES $log_file"
done

# Combine all log files into one file for email
cat $LOG_FILES > "$LOG_DIR/all_logs.txt"

# Email the log file
mail -s "Periodic Server Update Report" "$ReportToEmail" -r "$SenderEmail" < "$LOG_DIR/all_logs.txt"
