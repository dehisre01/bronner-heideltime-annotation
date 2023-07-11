#! /bin/sh
# install other requirements
pip install -r requirements.txt

mkdir data

# install python_heideltime
cd python_heideltime

chmod +x install_heideltime_standalone.sh
./install_heideltime_standalone.sh

python3 -m pip install .

