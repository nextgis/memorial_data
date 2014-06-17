# -*- encoding: utf-8 -*-
# ---------------------------------------------------------------------------
# mos_memo_ru_addresses.py
# Author: Maxim Dubinin (sim@gis-lab.info)
# About: Grabber for mos.memo.ru data on people executed in Moscow
# Created: 20.10.2013
# Usage example: 
#       grab all: python mos_memo_ru_addresses.py
# ---------------------------------------------------------------------------

import csv
import urllib2
import os
from bs4 import BeautifulSoup

def download_page(link,id):
    u = urllib2.urlopen(link)
    f = open("data/pages/" + id + ".htm","wb")
    f.write(u.read())
    f.close()
    print("Page for " + id + " was downloaded")

def parse_page(id):
    f_page = open("data/pages/" + id + ".htm",'rb')
    soup = BeautifulSoup(''.join(f_page.read()))
    streets = soup.findAll("p", { "class" : "Street" })
    tables = soup.findAll("table")
    
    for i in range(len(tables)):
        street = streets[i].strings.next()
        street_anchor = streets[i].find('a')['name']
        table = tables[i]
        for tr in table.findAll("tr"):
            tds = tr.findAll("td")
            for td in tds:
                try: 
                    person_count = td['rowspan']
                    house = tds[0].strings.next()
                    apt = tds[1].strings.next().replace(u" кв.","")
                    ss = [s for s in tds[2].strings]
                    name = ss[0]
                    bio = ss[1][2:]
                    link = url + "#" + street_anchor
                    csvwriter.writerow(dict(
                                            ADDRESS=(street.replace("   "," ") + ", " + house).encode("utf-8"),
                                            APT = apt.encode("utf-8"),
                                            NAME = name.encode("utf-8"),
                                            BIO = bio.encode("utf-8"),
                                            COUNT=person_count,
                                            LINK=link))
                except:
                    continue

if __name__ == '__main__':   
    f_output = open('data/all.csv', 'wb')
    fieldnames_data = ('ADDRESS','APT','NAME','BIO','COUNT','LINK')

    f_output.write(','.join(fieldnames_data) + "\n")
    csvwriter = csv.DictWriter(f_output, fieldnames=fieldnames_data)
    
    if not os.path.exists("data/pages"):
        os.makedirs("data/pages")
    
    for id in range(1,78):
        url = "http://mos.memo.ru/shot-" + str(id) + ".htm"
        download_page(url,str(id))
        parse_page(str(id))
    
    f_output.close()
