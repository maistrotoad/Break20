echo "Updating Break20"

CURRENT_DIR="$(pwd)"
INSTALL_DIR="$HOME/.local/share/maistrotoad/Break20"

echo "Copying src files to $INSTALL_DIR"
cp src/* "$INSTALL_DIR"

echo "Updating Python3  dependencies in venv"
cd "$INSTALL_DIR"
. venv/bin/activate
pip3 install -r requirements.txt

echo "Adding path to python3 venv to main.py so crontab can run it"
echo -e '#!'"$INSTALL_DIR/venv/bin/python3\n$(cat main.py)" >"$INSTALL_DIR/main.py"

echo "Trying to run Break20 once"
python3 main.py
cd "$CURRENT_DIR"
