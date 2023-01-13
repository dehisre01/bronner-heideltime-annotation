from standoffconverter import Standoff, View
from python_heideltime import Heideltime
from bs4 import BeautifulSoup as bs
import bs4
from lxml import etree
from tqdm import tqdm
import utils
import re
import os


heideltime_parser = Heideltime()
heideltime_parser.set_output_type('XMI') # default = TimeML
heideltime_parser.set_language('GERMAN') # default = english
heideltime_parser.set_document_time('1810-01-01') # default = today

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
    timeparsed = heideltime_parser.parse(plain)
    p = etree.XMLParser(huge_tree=True)
    # the results are parsed as lxml etree
    time_tree = etree.fromstring(bytes(timeparsed, encoding='utf-8'), parser=p)
    # this xpath expression filters for timeelements
    time_elements = time_tree.xpath("//heideltime:Timex3[@timexValue]",
        namespaces={"heideltime":"http:///de/unihd/dbs/uima/types/heideltime.ecore"})


    # this loop iterates over all by heideltime detected timeinstances and writes them into the standoff representation of our TEI file
    # following our annotation scheme
    for i in tqdm(time_elements, desc="writing time annotations"):
        # check if theres allready an entry at the position of the given annotation
        if (view.get_table_pos(int(i.attrib['begin'])) in so.table.df.position.values) and (view.get_table_pos(int(i.attrib['end'])) in so.table.df.position.values):
        # print("+++++string has allready been annotated!+++++")
            pass
        # references, like "PRESENT_REF" in the text e.g. "jetzt" have no value for us
        elif "_REF" in i.attrib['timexValue']:
            #print("+++++computed time is not wanted (Referenz)!+++++")
            pass
        else:
            if i.attrib['timexType'] == "DATE":
                if int(i.attrib['timexValue'][:4]) < 1800: 
                    # constraint to avoid 4 digit numbers from beeing falsely annotated as date (e.g. 1000 Rubel)
                    # this means at the same time that dates earlier than 1800 will not be annotated at all
                    pass
                elif ("-SU" or "-FA" or "-WI" or "-SP") in i.attrib['timexValue']:
                    # print("Annotation of season, will be skipped")
                    pass
                else:
                    so.add_inline(
                    begin=view.get_table_pos(int(i.attrib['begin'])),
                    end=view.get_table_pos(int(i.attrib['end'])),
                    tag='date',
                    depth=3,
                    attrib={'when':i.attrib['timexValue'],
                    'calendar':'#julian'} # julian is set as default calendar
                    )
            else:
                if "P" in i.attrib['timexValue']: # a value starting with P is a clear indication for a duration
                    if "X" in i.attrib['timexValue']: # a value including PX is an undefined time,
                        # which is not in our interest and therefore excluded
                        pass
                    else:
                        so.add_inline(
                        begin=view.get_table_pos(int(i.attrib['begin'])),
                        end=view.get_table_pos(int(i.attrib['end'])),
                        tag='time',
                        depth=3,
                        attrib={'dur':i.attrib['timexValue']}
                        )
                else:
                    # this matches patterns like "1810-02-15T05:00"
                    if re.match(r"\d{4}(-\d{2})+", i.attrib['timexValue']):
                        so.add_inline(
                        begin=view.get_table_pos(int(i.attrib['begin'])),
                        end=view.get_table_pos(int(i.attrib['end'])),
                        tag='time',
                        depth=3,
    # instead of a pattern like "1810-02-15T05:00" only the time "05:00:00+01:00" is written as value of the "when" attribute
                        attrib={'when': f"{i.attrib['timexValue'][-5:]}:00+01:00"}
                        )
                    else:
                        so.add_inline(
                        begin=view.get_table_pos(int(i.attrib['begin'])),
                        end=view.get_table_pos(int(i.attrib['end'])),
                        tag='time',
                        depth=3,
                        attrib={'when':f"{i.attrib['timexValue']}:00+01:00"}
                        )
    
    
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