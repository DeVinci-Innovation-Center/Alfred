#/bin/bash

VENV_NAME=".test_venv"

echo "install.sh should be run at the root of the git directory to avoid spraying files everywhere. Press enter to confirm or Ctrl+C to quit"

read enter

echo "creating virtual environment"
sleep 0.5

python3 -m venv $VENV_NAME

echo "virtual environment created"
sleep 0.5
echo "installing dependencies"
sleep 0.5

$VENV_NAME/bin/pip3 install -r requirements.txt

echo "dependecies installed"
sleep 0.5
echo "activate virtual environment with:\n\
    source $VENV_NAME/bin/activate"

echo "deactivate with:\n\
    deactivate\n\
after use"
