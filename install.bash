#!/usr/bin/env bash
if [ -z "$(which python3)" ]; then
    echo "You need to install python3 to be able to use this application ('which python3' turned up empty)"
    exit 1
fi

if [ -z "$(which crontab)" ]; then
    echo "You need to install crontab to be able to use this application ('which crontab' turned up empty)"
    exit 1
fi

echo "This install script is not idempotent; it will add a cronjob to your crontab"

echo "Creating venv"
python3 -m venv venv && . venv/bin/activate

echo "Installing Python3  dependencies in venv"
pip3 install -r requirements.txt

echo "Adding path to python3 venv to main.py so crontab can run it"
CURRENT_DIR="$(pwd)"
echo -e "#!"$CURRENT_DIR/venv/bin/python3"\n$(cat main.py)" >main.py

echo "Adding cronjob to crontab to run every 20 minutes"
crontab -l | {
    cat
    echo "SHELL=$(which bash)"
    echo "*/20 * * * * DISPLAY=:1 XAUTHORITY=/run/user/1000/gdm/Xauthority '$CURRENT_DIR/main.py' > /tmp/cronlog.tmp 2>&1"
} | crontab -

echo "Trying to run Break20 once"
python3 main.py
