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
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'ghtk',
}

# FILE MAPPING PROVINCE:
PAIR_PROVINCE       = "province_pair.txt"
MAP_ALL_PROVINCE    = "province_name.csv"
FILE_MAP_OUT        = "mapping_output.csv"

PATTERNS = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

PREFIX = {
    'huyện ': 'h ',
    'quận ': 'q ',
    'thị xã ': 'tx ',
    'thành phố ': 'tp ',
    'xã ':  'x',
    'phường ': 'p',
    'thị trấn ': 'tt',
    'đường '     : 'd'
}

def convert_non_accented(text):
    
    output = text

    for key, value in PREFIX.items():
        output = output.replace(key, value)
    for regex, replace in PATTERNS.items():
        output = re.sub(regex, replace, output)
    return output

def addr_similar(a, b):

    a = convert_non_accented(a.lower())
    b = convert_non_accented(b.lower())
    return SequenceMatcher(None, a, b).ratio()

def connect_db(cnx,config_db,  query):
    
    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result


def main():
    cnx = mysql.connector.connect(**CONFIG_DB)
    mapping_result = []
    for line in open(MAP_ALL_PROVINCE).readlines():
        line = line[:-1].split(",")
        mapping_result.append(line)

    pairs = [l.split() for l in open(PAIR_PROVINCE).readlines()]
    queue = deque(pairs)
    while (len(queue) != 0):
        pair_address = queue.popleft()

        # address_service_id, name, prefix, parent_name, _type
        query1 = """
            SELECT ad.id, ad._name, ad._prefix, ad1._name as parent_name, ad._type  
            FROM ghtk.address_service ad 
            LEFT JOIN ghtk.address_service ad1 on ad.parent_id = ad1.id
            WHERE ad.parent_id =""" + str(pair_address[1])  # BANG NAY CHUAN HON, 46767 ROWS
        address_1 = connect_db(cnx, CONFIG_DB, query1)
        # print("Q1", query1)
        if not address_1:
            continue
        
        # Address_id, address_name, address_type, address_parent
        query2 = """
            SELECT ad.id, ad.name, ad.type, ad1.name as parent_name  
            FROM ghtk.addresses ad 
            LEFT JOIN ghtk.addresses ad1 on ad.parent_id = ad1.id
            WHERE ad.parent_id =""" + str(pair_address[0])   # BANG NAY CUA GHTK, 23484 ROWS
        address_2 = connect_db(cnx,CONFIG_DB, query2)
        # print("Q2", query2)
        if not address_2:
            continue
        for add_1 in address_1:
            temp_pairs = {}
            for add_2 in address_2:
                if (add_1[4] != add_2[2]):
                    continue
                simillar = addr_similar(add_1[1], add_2[1])
                if( simillar > 0.7):
                    temp_pair = [add_2[0], add_1[0], add_2[1], add_1[1], add_2[2], add_1[2], add_2[3], add_1[3] ]
                    temp_pairs[simillar] = temp_pair
            if not temp_pairs:
                continue
            max_simillar = max(temp_pairs.keys())
            new_pair = temp_pairs[max_simillar]
            # print("new pair:", new_pair)
            append_pair = [new_pair[0], new_pair[1]]
            queue.append(append_pair)
            mapping_result.append([new_pair[0], new_pair[1], new_pair[2], new_pair[3], new_pair[4], new_pair[5], new_pair[6], new_pair[7], round(max_simillar,3)] )
    print("Total: ", len(mapping_result))
    with open(FILE_MAP_OUT, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(mapping_result)

    csvFile.close()
    cnx.close()
        

start_time = time.time()
main()
elapsed_time = time.time() - start_time
print("\n------ Elapsed time: " + str(round(elapsed_time, 3)) + "s ------")

