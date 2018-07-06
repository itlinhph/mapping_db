#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- Author: LinhPH ---
import csv
import mysql.connector
import re
import time
from difflib import SequenceMatcher
from collections import deque

CONFIG_DB_FULL = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'ghtk',
}

CONFIG_DB_DEVTUAN = {
    'user': 'linhph',
    'password': 'acf5f498c914e8fea7dec29219a1e4fc',
    'host': '10.6.0.1',
    'database': 'dev_tuannn',
}

# FILE MAPPING PROVINCE:
PAIR_PROVINCE       = "province_pair.txt"
MAP_ALL_PROVINCE    = "province_name.txt"
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

def connect_db(config_db,  query):
    # Connect database:
    cnx = mysql.connector.connect(**config_db)

    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cnx.close()
    return result


def main():
    mapping_result = []
    for line in open(MAP_ALL_PROVINCE).readlines():
        line = line[:-1].split(",")
        mapping_result.append(line)

    pairs = [l.split() for l in open(PAIR_PROVINCE).readlines()]
    queue = deque(pairs)
    while (len(queue) != 0):
        pair_address = queue.popleft()
        
        query1 = "Select id, _name From address_service Where parent_id =" + str(pair_address[0])
        address_1 = connect_db(CONFIG_DB_FULL, query1)
        if not address_1:
            continue
        query2 = "Select id, name From addresses Where parent_id =" + str(pair_address[1])
        address_2 = connect_db(CONFIG_DB_DEVTUAN, query2)
        if not address_2:
            continue
        for add_1 in address_1:
            temp_pairs = {}
            for add_2 in address_2:
                simillar = addr_similar(add_1[1], add_2[1])
                if( simillar > 0.7):
                    temp_pair = [add_1[0], add_1[1], add_2[0], add_2[1] ]
                    temp_pairs[simillar] = temp_pair
            if not temp_pairs:
                continue
            max_simillar = max(temp_pairs.keys())
            new_pair = temp_pairs[max_simillar]
            # print("new pair:", new_pair)
            append_pair = [new_pair[0], new_pair[2]]
            queue.append(append_pair)
            mapping_result.append([new_pair[0], new_pair[1], new_pair[2], new_pair[3], pair_address[0], round(max_simillar,3)] )
    print("Total: ", len(mapping_result))
    with open(FILE_MAP_OUT, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(mapping_result)

    csvFile.close()
        

start_time = time.time()
main()
elapsed_time = time.time() - start_time
print("\n------ Elapsed time: " + str(round(elapsed_time, 3)) + "s ------")

