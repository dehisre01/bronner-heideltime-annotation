# bronner-time-annotations

This module uses the python-wrapper for the time annotation tool "Heideltime" and enables the processing of a TEI XML file using the python library "standoffconverter".
It also filters and refines the generated annotations using RegEx patterns to better fit our specific text, which is an early 19th century German travelogue by Franz Xaver Bronner.

It runs on a Linux system or a Linux subsystem such as WSL.

# Usage

For the installation we provide a script called `install-heideltime.sh`. Before installing Python_Heideltime, you need to install HeidelTime-standalone, which can be downloaded from Heideltime's [releases page](https://github.com/HeidelTime/heideltime/releases). This module supports version 2.2.1. After installing HeidelTime-standalone, you can install the requirements for this module by navigating to the top-level folder `heidel time` and running the script in your console:

```install-heideltime.sh
bash install-heideltime.sh
```

Now the heideltime python-wrapper should be installed, along with the other dependencies for this module. There is also a folder called `data` where you should put all the XML files you want to annotate.

After placing all XML files in the `data` folder, start the `main.py` script by typing the following command in your console:

```python
python3 main.py
```

The annotated XML files should be saved in the `data` folder in the following format: `name_of_your_file`_timeparsed.xml.

# Submodule python_heideltime

[https://github.com/PhilipEHausner/python_heideltime](https://github.com/PhilipEHausner/python_heideltime)

# standoffconverter

[https://github.com/standoff-nlp/standoffconverter](https://github.com/standoff-nlp/standoffconverter)
