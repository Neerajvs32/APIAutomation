#!/bin/bash

# Setup cron job to run CertifyMe API automation at 7am IST (1:30 UTC) daily

SCRIPT_PATH="/home/adithya/Desktop/Unit testing/APIAutomation/cred.py"
LOG_FILE="/home/adithya/Desktop/Unit testing/APIAutomation/cron.log"

# Cron schedule: 30 1 * * * (1:30 UTC = 7:00 IST)
CRON_SCHEDULE="30 1 * * *"

# Python command
PYTHON_CMD="/usr/bin/python3"

# Full command
COMMAND="$PYTHON_CMD \"$SCRIPT_PATH\" >> \"$LOG_FILE\" 2>&1"

# Check if cron job already exists
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH" || echo "")

if [ -n "$EXISTING_CRON" ]; then
    echo "Cron job already exists:"
    echo "$EXISTING_CRON"
    echo "Remove it first if you want to update."
    exit 1
fi

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $COMMAND") | crontab -

echo "Cron job added successfully!"
echo "Will run daily at 7:00 AM IST (1:30 AM UTC)"
echo "Output will be logged to: $LOG_FILE"

# Verify
echo "Current crontab:"
crontab -l