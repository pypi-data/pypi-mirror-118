#!/bin/bash
if ! hash python; then
    echo "python is not installed"
    exit 1
fi

ver=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "37" ]; then
    echo "Famcy requires python 3.7 or greater"
    exit 1
fi

sudo apt-get install python3-venv
mkdir -p ~/.local/share/famcy/$1/console
cd ~/.local/share/famcy/$1
python3 -m venv venv
source venv/bin/activate
pip3 install wheel uwsgi
pip3 install setuptools-rust
pip3 install famcy

wget https://gadgethi-css.s3.amazonaws.com/FamcyConsole.zip
tar -xf FamcyConsole.zip
mv FamcyConsole console
rm FamcyConsole.zip

echo 'alias activate_$1="source ~/.local/share/famcy/$1/venv/bin/activate"'