# bronner-time-annotations

This module uses the time annotation tool "HeidelTime" to annotate temporal expressions in narrative texts. Input- and outputformat are TEI-XML. It filters and refines the generated annotations using RegEx patterns to better fit our specific text, which is an early 19th century German travelogue by Franz Xaver Bronner.
It makes use of ```py-heideltime``` python_wrapper of HeidelTime and ```standoffconverter``` to facilitate the TEI-XML file(s).

# Usage

Install the requirements by run the following command in your terminal:

```bash
pip install requirements.txt
```

After placing all XML files in the `data` folder, start the `main.py` script by typing the following command in your console:

```python
python3 main.py
```

The annotated XML files should be saved in the `data` folder in the following format: `name_of_your_file`_timeparsed.xml.
# HeidelTime
Project Homepage: [https://dbs.ifi.uni-heidelberg.de/research/heideltime/](https://dbs.ifi.uni-heidelberg.de/research/heideltime/)

GitHub: [https://github.com/HeidelTime/heideltime](https://github.com/HeidelTime/heideltime)

# py-heideltime

[https://github.com/hmosousa/py_heideltime](https://github.com/hmosousa/py_heideltime)

# standoffconverter

[https://github.com/standoff-nlp/standoffconverter](https://github.com/standoff-nlp/standoffconverter)


