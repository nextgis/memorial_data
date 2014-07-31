# -*- encoding: utf-8 -*-
# ---------------------------------------------------------------------------
# mos_memo_ru_addresses.py
# Author: Maxim Dubinin (sim@gis-lab.info)
# About: Grabber for mos.memo.ru data on people executed in Moscow, creates two tables: persons and addresses linked by address ID
# Created: 20.10.2013
# Updated: 31.07.2014
# Usage example: 
#       grab all: python mos_memo_ru_addresses.py
# ---------------------------------------------------------------------------

import csv
import urllib2
import os
from bs4 import BeautifulSoup

def download_page(link,id):
    u = urllib2.urlopen(link)
    f = open("data/mos.memo.ru/pages/" + id + ".htm","wb")
    f.write(u.read())
    f.close()
    print("Page for " + id + " was downloaded")

def parse_page(id, address_id):
    f_page = open("data/mos.memo.ru/pages/" + id + ".htm",'rb')
    soup = BeautifulSoup(''.join(f_page.read()))
    streets = soup.findAll("p", { "class" : "Street" })
    tables = soup.findAll("table")

    for i in range(len(tables)):
        street = streets[i].strings.next()
        street_anchor = streets[i].find('a')['name']
        table = tables[i]
        for tr in table.findAll("tr"):
            tds = tr.findAll("td")

            if 'rowspan' in str(tds[0]):
                address_id = address_id + 1
                print address_id
                apt_count = tds[0]['rowspan']
                if tds[0].find("p"):
                    person_count = tds[0].find("p").text.replace(u" чел.","")
                else:
                    person_count = 1
                
                house = tds[0].strings.next()
                apt = tds[1].strings.next().replace(u" кв.","")
                persons = tds[2].findAll("p")
                link = url + "#" + street_anchor
                
                csvwriter_addr.writerow(dict(
                                    ADDRESS_ID=address_id,
                                    ADDRESS=(street.replace("   "," ") + ", " + house).encode("utf-8"),
                                    APT_COUNT=apt_count,
                                    PERS_COUNT=person_count,
                                    LINK=link))
            else:
                #house is assigned beforehand
                apt = tds[0].strings.next().replace(u" кв.","")
                persons = tds[1].findAll("p")
                link = url + "#" + street_anchor

            for person in persons:

                ss = person.text.split(",")
                name = ss[0]
                print name
                bio = ",".join(ss[1:]).strip()

                csvwriter_main.writerow(dict(
                                        ADDRESS_ID=address_id,
                                        APT = apt.encode("utf-8"),
                                        NAME = name.encode("utf-8"),
                                        BIO = bio.encode("utf-8"),
                                        LINK=link))
    return address_id

if __name__ == '__main__':   
    f_output_main = open('data/mos.memo.ru/persons.csv', 'wb')
    f_output_addr = open('data/mos.memo.ru/addresses.csv', 'wb')
    
    fieldnames_main = ('ADDRESS_ID','APT','NAME','BIO','LINK')
    fieldnames_addr = ('ADDRESS_ID','ADDRESS','APT_COUNT','PERS_COUNT','LINK')

    f_output_main.write(','.join(fieldnames_main) + "\n")
    f_output_addr.write(','.join(fieldnames_addr) + "\n")
    
    csvwriter_main = csv.DictWriter(f_output_main, fieldnames=fieldnames_main)
    csvwriter_addr = csv.DictWriter(f_output_addr, fieldnames=fieldnames_addr)
    
    if not os.path.exists("data/mos.memo.ru/pages"):
        os.makedirs("data/mos.memo.ru/pages")
    
    address_id = 0

    for id in range(1,79):
        url = "http://mos.memo.ru/shot-" + str(id) + ".htm"
        download_page(url,str(id))
        address_id = parse_page(str(id), address_id)
    
    f_output_main.close()
