from py_heideltime import heideltime
from standoffconverter import Standoff, View
from bs4 import BeautifulSoup as bs
import bs4
from lxml import etree
from tqdm import tqdm
import utils
import re
import os

ns = "http://www.tei-c.org/ns/1.0"

for file in os.listdir("data"):
    print(file, " is beeing processed.")
    try:
    # intercept deficient XML or non-XML files
        tree =  etree.parse(f"data/{file}")
    except:
        print("file has no valid XML format.")
        continue

    so = Standoff(tree, namespaces={"tei":ns})

    view = (
        View(so)
            .shrink_whitespace()
            .exclude_inside(ns+"note") # the content of note tags is excluded from the view
            .exclude_inside(ns+"abbr") # the content of abbr tags is excluded from the view
    #        .exclude_inside(ns+"expan") # the content of expan tags is excluded from the view
    )

    # creates a plaintext version of the annotated tree
    plain = view.get_plain()
    # the plaintext is parsed for time occurences using heideltime,
    # the output format is XMI since it bears information on begin and end of the time occurence
    timexs = heideltime(plain, language="german", document_type="narrative", dct="1810-01-01")
#"""  p = etree.XMLParser(huge_tree=True)
 #   # the results are parsed as lxml etree
  #  time_tree = etree.fromstring(bytes(timeparsed, encoding='utf-8'), parser=p)
    # this xpath expression filters for timeelements
   # time_elements = time_tree.xpath("//heideltime:Timex3[@timexValue]",
    #    namespaces={"heideltime":"http:///de/unihd/dbs/uima/types/heideltime.ecore"})"""


    # this loop iterates over all by heideltime detected timeinstances and writes them into the standoff representation of our TEI file
    # following our annotation scheme
    for i in tqdm(timexs, desc="writing time annotations"):
        # check if theres allready an entry at the position of the given annotation
        if (view.get_table_pos(int(i["span"][0])) in so.table.df.position.values) and (view.get_table_pos(int(i["span"][1])) in so.table.df.position.values):
            print("+++++string has allready been annotated!+++++")
            pass
        # references, like "PRESENT_REF" in the text e.g. "jetzt" have no value for us
        elif "_REF" in i["value"]:
            print("+++++computed time is not wanted (Referenz)!+++++")
            pass
        elif i["type"] == "SET":
            print("+++++computed time is not wanted (Set)!+++++")
            pass
        else:
            # search and filter flawed dates
            if i["type"] == "DATE":
                if int(i['value'][:4]) < 1800: 
                    # constraint to avoid 4 digit numbers from beeing falsely annotated as date (e.g. 1000 Rubel)
                    # this means at the same time that dates earlier than 1800 will not be annotated at all
                    pass
                elif ("-SU" or "-FA" or "-WI" or "-SP") in i["value"]:
                    print("Annotation of season, will be skipped")
                    pass
                else:
            # write filtered dates in the standoff annotation table
                    try:
                        so.add_inline(
                        begin=view.get_table_pos(int(i["span"][0])),
                        end=view.get_table_pos(int(i["span"][1])),
                        tag="date",
                        #depth=3,
                        attrib={"when":i["value"],
                        "calendar":"#julian"} # julian is set as default calendar
                        )
                    except:
                        print("eintrag in so tabelle gescheitert")
            else:
                if "P" in i["value"]: # a value starting with P is a clear indication for a duration
                    if "X" in i["value"]: # a value including PX is an undefined time,
                        # which is not in our interest and therefore excluded
                        pass
                    else:
                        try:
                            so.add_inline(
                            begin=view.get_table_pos(int(i["span"][0])),
                            end=view.get_table_pos(int(i["span"][1])),
                            tag="time",
                            #depth=3,
                            attrib={"dur":i["value"]}
                            )
                        except:
                            print("eintrag in so tabelle gescheitert")
                else:
                    # this matches patterns like "1810-02-15T05:00"
                    if re.match(r"\d{4}(-\d{2})+", i["value"]):
                        try:
                            so.add_inline(
                            begin=view.get_table_pos(int(i["span"][0])),
                            end=view.get_table_pos(int(i["span"][1])),
                            tag="time",
                            #depth=3,
        # instead of a pattern like "1810-02-15T05:00" only the time "05:00:00+01:00" is written as value of the "when" attribute
                            attrib={"when": f"{i['value'][-5:]}:00+01:00"}
                            )
                        except:
                            print("eintrag in so tabelle gescheitert")
                    else:
                        try:
                            so.add_inline(
                            begin=view.get_table_pos(int(i["span"][0])),
                            end=view.get_table_pos(int(i["span"][1])),
                            tag="time",
                            #depth=3,
                            attrib={"when":f"{i['value']}:00+01:00"}
                            )
                        except:
                            print("eintrag in so tabelle gescheitert")
    
    
    new_filename = re.match('.*?((?=\.)|$)', file).group() + "_timeparsed.xml"

    so.tree.write(f'data/{new_filename}', encoding='utf-8')


    with open(f'data/{new_filename}', 'r', encoding='utf-8') as file:
        doc = file.read()

    soup = bs(doc, 'lxml-xml')

    # the dates are refined by searching for patterns in front of the detected time annotations
    soup = utils.refine_dates(soup)
    # the times are refined by searching for patterns in front of the detected time annotations
    soup = utils.refine_time(soup)

    with open(f'data/{new_filename}', 'w') as f:
        f.write(soup.encode(formatter='minimal').decode('utf-8'))
