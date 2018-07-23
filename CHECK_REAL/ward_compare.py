#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Author: LinhPH ---
import csv
import mysql.connector
import re
import time
from difflib import SequenceMatcher
from collections import deque


CONFIG_DB = {
    'user': 'linhph',
    'password': '',
    'host': 'localhost',
    'database': 'ghtk',
}

REPLACE = {
    'òa': 'oa',
    'oà' : 'oa',
    'uỷ' : 'uy',
    'ủy' : 'uy'
}

# FILE MAPPING PROVINCE:
PAIR_PROVINCE       = "data/district_pair.csv"
FALSE_WARD          = "data/false_ward.csv"
FILE_MAP_OUT        = "ward_mapping_out.csv"


def connect_db(cnx,config_db,  query):
    
    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result


def addr_similar(a, b):
    a = a.lower()
    a = " ".join(a.split())
    b = b.lower()
    b = " ".join(b.split())
    for regex, replace in REPLACE.items():
        a = re.sub(regex, replace, a)
        b = re.sub(regex, replace, b)
    simillars = SequenceMatcher(None, a, b).ratio()
    # print( a,"---", b, simillars )
    return simillars

def compare_district(cnx, pair):
    
    # db16: ID, NAME, PREFIX, DISTRICT_ID, P_NAME
    query1 = """
        SELECT x.xaid, x.name, x.type, x.maqh, q.name FROM ghtk.devvn_xaphuongthitran x, ghtk.devvn_quanhuyen q
        where x.maqh = q.maqh 
        and x.maqh =""" + pair[0] 
    address_1 = connect_db(cnx, CONFIG_DB, query1)
    
    # AS: ID, NAME, PREFIX, DISTRICT_ID, P_NAME, PROVINCE_ID
    query2 = """
        SELECT w.id, w._name, w._prefix, w._district_id, d._name as p_name, w._province_id FROM ghtk.ward w, ghtk.district d
        where w._district_id = d.id
        and w._district_id =""" + pair[1]
    address_2 = connect_db(cnx,CONFIG_DB, query2)

    return address_1, address_2


def main():
    cnx = mysql.connector.connect(**CONFIG_DB)
    mapping_result = [["DB16_ID", "AS_ID", "DB16_NAME","DB16_PREFIX", "AS_NAME", "AS_PREFIX", "P_ID", "PROVINCE_ID", "P_NAME", "NOTE"]]

    pairs = [l.split() for l in open(PAIR_PROVINCE).readlines()]
    ward_false = [l.split() for l in open(FALSE_WARD).readlines()]
    
    for pair_address in pairs:
        
        address_1, address_2 = compare_district(cnx, pair_address)        
        addr2_mapped = []
        for add_1 in address_1:
            found_pair = False
            new_pair = []
            max_simillar = 0
            for add_2 in address_2:
                if(found_pair):
                    continue
                full_name = add_2[2] + " " + add_2[1]

                if(add_1[1] == full_name):
                    new_pair = [add_1[0], add_2[0], add_1[1].replace(add_1[2]+" ", ""), add_1[2], add_2[1], add_2[2], add_2[3],add_2[5], add_2[4], "1"]
                    found_pair = True
                    
                elif(add_1[1].replace(add_1[2]+" ", "") == add_2[1] ):
                    new_pair = [add_1[0], add_2[0], add_1[1].replace(add_1[2]+" ", ""), add_1[2], add_2[1], add_2[2], add_2[3], add_2[5], add_2[4], "Sai prefix"]
                    found_pair = True
                else:
                    # print(str(add_1[0]) + "\t" + str(add_2[0]))
                    simillar = addr_similar(add_1[1] ,full_name)
                    if(simillar > max_simillar and [add_1[0], str(add_2[0])] not in ward_false):
                        max_simillar = simillar
                        new_pair = [ add_1[0], add_2[0], add_1[1].replace(add_1[2]+" ", ""), add_1[2], add_2[1], add_2[2], add_2[3], add_2[5], add_2[4],round(simillar,3) ]
                        

            if(found_pair or max_simillar > 0.79):
                mapping_result.append(new_pair)
                addr2_mapped.append((new_pair[1], new_pair[4], new_pair[5], new_pair[6], new_pair[8], new_pair[7]))
                # print(new_pair)
            else:
                db16_alone = [add_1[0], "", add_1[1], add_1[2], "", add_1[2], add_1[3],"", add_1[4], ""]
                mapping_result.append(db16_alone)
        for item in address_2:
            if item not in addr2_mapped:
                null_pair = ["", item[0], "", "", item[1], item[2], item[3], item[5], item[4], ""]
                mapping_result.append(null_pair)
                # print(null_pair)

    print("Total: ", len(mapping_result))
    with open(FILE_MAP_OUT, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(mapping_result)

    csvFile.close()
    cnx.close()
        



start_time = time.time()
main()
elapsed_time = time.time() - start_time
print("\n------ Elapsed time: " + str(round(elapsed_time, 3)) + " s ------")
