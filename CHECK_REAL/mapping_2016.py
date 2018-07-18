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
MAP_ALL_PROVINCE    = "province_all_2016.csv"
FILE_MAP_OUT        = "mapping_out_2016.csv"


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


def main():
    cnx = mysql.connector.connect(**CONFIG_DB)
    mapping_result = []
    for line in open(MAP_ALL_PROVINCE).readlines():
        line = line[:-1].split(",")
        mapping_result.append(line)

    pairs = [l.split() for l in open(PAIR_PROVINCE).readlines()]
    
    queue = deque(pairs)

    # get all ads_id and ad_16_id
    query_ads = "SELECT id FROM ghtk.db_ads"
    result = connect_db(cnx, CONFIG_DB, query_ads)
    ads_id = []
    for item in result:
        ads_id.append(item[0])

    # print(ads_id)
    query_16 = "SELECT id FROM ghtk.devvn_2016_12"
    result = connect_db(cnx, CONFIG_DB, query_16)
    db16_id = []
    for item in result:
        db16_id.append(item[0])
    
    print(type(db16_id), len(db16_id))
    ads_mapped = []
    db16_mapped = []
    
    num_continue =0
    while (len(queue) != 0 and num_continue <40):
        pair_address = queue.popleft()
        
        # address_service_id, name, prefix, parent_id, parent_name, type
        query1 = """
            SELECT ad.id, ad.name, ad.prefix, ad.parent_id, ad1.name as parent_name, ad.type  
            FROM ghtk.db_ads ad 
            LEFT JOIN ghtk.db_ads ad1 on ad.parent_id = ad1.id
            WHERE ad.parent_id =""" + str(pair_address[1])  # BANG NAY CUA ADDRESS SERVICE
        address_1 = connect_db(cnx, CONFIG_DB, query1)
        if not address_1:
            num_continue +=1
            continue

        # dev2016_id, name, prefix, parent_id, parent_name
        query2 = """
            SELECT ad.id, ad.name, ad.prefix, ad.parent_id, ad1.name as parent_name  
            FROM ghtk.devvn_2016_12 ad 
            LEFT JOIN ghtk.devvn_2016_12 ad1 on ad.parent_id = ad1.id
            WHERE ad.parent_id =""" + str(pair_address[0])   # BANG NAY CUA dev_2016
        address_2 = connect_db(cnx,CONFIG_DB, query2)
        
        for add_1 in address_1:
            for add_2 in address_2:
                have_pair = False
                full_addr = add_1[2] + " " + add_1[1]
                # simmilar = addr_similar(full_addr, add_2[1])
                
                if(full_addr == add_2[1]):
                    note = "1"
                    have_pair = True
                elif (add_1[1] in add_2[1] and add_1[2] != add_2[2] and len(add_1[1]) >1):
                    note = "False Prefix"
                    have_pair = True
                elif (addr_similar(full_addr, add_2[1])> 0.9):
                    note = "Similar"
                    have_pair = True

                if have_pair == True:
                    new_mapping = [add_2[0], add_1[0], add_2[1], add_1[1], add_1[2], add_1[3], add_1[4], add_1[5], note ]
                    mapping_result.append(new_mapping)
                    print("newpair:", new_mapping)
                    queue.append([add_2[0], add_1[0]])
                    ads_mapped.append(add_1[0])
                    db16_mapped.append(add_2[0])
                    num_continue = 0

    ads_not_mapped = list(set(ads_id) - set(ads_mapped))
    db16_not_mapped = list(set(db16_id) - set(db16_mapped))

    print("ads no infor:", len(ads_not_mapped))
    print("db16 no infor:", len(db16_not_mapped))

    for id in ads_not_mapped:
        query1 = """
            SELECT ad.id, ad.name, ad.prefix, ad.parent_id, ad1.name as parent_name, ad.type  
            FROM ghtk.db_ads ad 
            LEFT JOIN ghtk.db_ads ad1 on ad.parent_id = ad1.id
            WHERE ad.type <> 0 
            AND ad.id =""" + str(id)
        result = connect_db(cnx, CONFIG_DB, query1)
        if not result:
            continue

        new_mapping = ["",result[0][0], "", result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], "NO INFOR ADS" ]
        # print("ads no info: ", new_mapping)
        mapping_result.append(new_mapping)

    for id in db16_not_mapped:
        query2 = """
            SELECT ad.id, ad.name, ad.prefix, ad.parent_id, ad1.name as parent_name  
            FROM ghtk.devvn_2016_12 ad 
            LEFT JOIN ghtk.devvn_2016_12 ad1 on ad.parent_id = ad1.id
            WHERE ad.id =""" + str(id)
        result = connect_db(cnx, CONFIG_DB, query2)
        new_mapping = [result[0][0], "", result[0][1], "", result[0][2], result[0][3], result[0][4], "NULL", "NO INFOR DB16" ]
        # print("db16 no info: ", new_mapping)
        mapping_result.append(new_mapping)


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

