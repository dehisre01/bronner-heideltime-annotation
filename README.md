# bronner-time-annotations

This module makes use of the python-wrapper for the java time annotation tool "Heideltime" and enables to work it on a TEI XML file by using the "standoffconverter" library.
It further filters and refines the automated annotations, by use of regex patterns, to fit better for our specific text, which is an early 19th century German travelogue by Franz Xaver Bronner.

It runs on a Linux System or a Linux Subsystem like WSL.

# Usage

We provide a script for installation called `install-heideltime.sh `. Before you can install the Python_Heideltime you need to install HeidelTime-standalone, which can be downloaded from Heideltime's [releases page](https://github.com/HeidelTime/heideltime/releases). This Module supports version 2.2.1. After you installed the HeidelTime-standalone, you can procede installing the requirements for this module by navigating to the top-level folder `heidel time` and type runing the script in your console:

```install-heideltime.sh
bash install-heideltime.sh
```

Now the Heideltime python-wrapper should be installed, along the other dependencies for this module. Furthermore there is a folder called `data`, where you can put all your XML files, you like to annotate.

After you stored all the files you like to annotate in the `data`-folder, run the `main.py` script, by typing the following command in your console:

```python
python3 main.py
```

The annotated files should be stored in the `data`-folder in the following format: name_of_your_file_timeparsed.xml.

# Submodule python_heideltime

[https://github.com/PhilipEHausner/python_heideltime]()

# standoffconverter

[https://github.com/standoff-nlp/standoffconverter]()
