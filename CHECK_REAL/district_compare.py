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

# FILE MAPPING PROVINCE:
PAIR_PROVINCE       = "province_pair_16.csv"
# PAIR_PROVINCE       = "data/district_pair.csv"
MAP_ALL_PROVINCE    = "province_all_2016.csv"
FILE_MAP_OUT        = "district_mapping_out.csv"


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
    # print("String process: ", a,b)
    simillars = SequenceMatcher(None, a, b).ratio()
    return simillars

def compare_district(cnx, pair):
    
    # db16: ID, NAME, PREFIX, PROVINCE_ID, P_NAME
    query1 = """
        SELECT q.maqh, q.name, q.type, q.matp, t.name FROM ghtk.devvn_quanhuyen q, ghtk.devvn_tinhthanhpho t
        where q.matp = t.matp
        and q.matp =""" + pair[0] 
    address_1 = connect_db(cnx, CONFIG_DB, query1)
    
    # AS: ID, NAME, PREFIX, PROVINCE_ID, P_NAME
    query2 = """
        SELECT d.id, d._name, d._prefix, d._province_id, p._name FROM ghtk.district d, ghtk.province p
        where d._province_id = p.id
        and d._province_id =""" + pair[1]
    address_2 = connect_db(cnx,CONFIG_DB, query2)

    return address_1, address_2


def main():
    cnx = mysql.connector.connect(**CONFIG_DB)
    mapping_result = [["DB16_ID", "AS_ID", "DB16_NAME", "AS_NAME", "PREFIX", "P_ID", "P_NAME", "NOTE"]]

    pairs = [l.split() for l in open(PAIR_PROVINCE).readlines()]
    
    # queue = deque(pairs)

    # while (len(queue) != 0 ):
    for pair_address in pairs:
        # pair_address = queue.popleft()
        address_1, address_2 = compare_district(cnx, pair_address)        
    
        for add_1 in address_1:
            found_pair = False
            new_pair = []
            max_simillar = 0
            for add_2 in address_2:
                if(found_pair):
                    continue
                if(add_2[3] ==1 and len(add_2[2])==0):
                    full_name = add_2[1]
                else:
                    full_name = add_2[2] + " " + add_2[1]

                if(add_1[1] == full_name):
                    new_pair = [add_1[0], add_2[0], add_1[1], add_2[1], add_2[2], add_2[3], add_2[4], "1"]
                    found_pair = True
                    
                elif(add_1[1].replace(add_1[2]+" ", "") == add_2[1] ):
                    new_pair = [add_1[0], add_2[0], add_1[1], add_2[1], add_2[2], add_2[3], add_2[4], "Sai prefix"]
                    found_pair = True
                else:
                    simillar = addr_similar(add_1[1] ,full_name)
                    if(simillar > max_simillar):
                        max_simillar = simillar
                        new_pair = [ add_1[0], add_2[0], add_1[1], add_2[1], add_2[2], add_2[3], add_2[4],round(simillar,3) ]
                        

            if(found_pair or max_simillar > 0.79):
                mapping_result.append(new_pair)
                # print(new_pair)
            else:
                new_pair = [add_1[0], "", add_1[1], "", add_1[2], add_1[3], add_1[4], ""]
                mapping_result.append(new_pair)
                # print("NULL")
                


    print("Total: ", len(mapping_result))
    with open(FILE_MAP_OUT, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(mapping_result)

    csvFile.close()
    cnx.close()
        



start_time = time.time()
main()
# get_wrong_address()
# a = addr_similar("Ecohome", "Ecohome Phúc Lợi")
# print(a)
elapsed_time = time.time() - start_time
print("\n------ Elapsed time: " + str(round(elapsed_time, 3)) + "s ------")

