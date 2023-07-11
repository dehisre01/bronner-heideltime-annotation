#! /bin/sh
# you need wheel to install heideltime
pip install wheel

# install python_heideltime
cd python_heideltime

chmod +x install_heideltime_standalone.sh
./install_heideltime_standalone.sh

python3 -m pip install .

# install other requirements
cd ..
pip install -r requirements.txt

mkdir data
