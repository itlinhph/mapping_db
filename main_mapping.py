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
PAIR_PROVINCE       = "data/province_pair.csv"
WRONG_ADDRESSES     = "data/wrong_addr.csv"
TRUE_ADDRESSES      = "data/true_addr.csv"
NOTSURE_ADDRESSES   = "data/notsure.csv"
MAP_ALL_PROVINCE    = "data/province_name.csv"
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
    'xã ':  'x ',
    'phường ': 'ph ',
    'thị trấn ': 'tt ',
    'đường '     : 'd ',
    # 'phố ' : 'p '
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
    a = " ".join(a.split())
    b = convert_non_accented(b.lower())
    b = " ".join(b.split())
    print("String process: ", a,b)
    simillars = SequenceMatcher(None, a, b).ratio()
    return simillars

def connect_db(cnx,config_db,  query):
    
    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result

def get_wrong_address():
    full_address = [line.rstrip('\n') for line in open('data/add_full.csv')]
    filter_address = [line.rstrip('\n') for line in open('data/add_filter.csv')]
    # print(filter_address)
    print(type(full_address), type(filter_address))
    wrong_addr = list(set(full_address) - set(filter_address))
    print(wrong_addr)
    with open('wrong_addr.csv', 'w') as filehandle:
        for listitem in wrong_addr:
            filehandle.write('%s\n' % listitem)

def load_checked_data(file_name):
    list_pairs = []
    for line in open(file_name).readlines():
        line = line[:-1].split("\t")
        list_pairs.append(list(map(int, line)))
    
    return list_pairs

def main():
    cnx = mysql.connector.connect(**CONFIG_DB)
    mapping_result = []
    for line in open(MAP_ALL_PROVINCE).readlines():
        line = line[:-1].split(",")
        mapping_result.append(line)

    pairs = [l.split() for l in open(PAIR_PROVINCE).readlines()]
    wrong_addrs = load_checked_data(WRONG_ADDRESSES)
    true_addrs = load_checked_data(TRUE_ADDRESSES)
    notsure_addrs = load_checked_data(NOTSURE_ADDRESSES)
    
    queue = deque(pairs)
    num_continue = 0
    while (len(queue) != 0 and num_continue < 40):
        pair_address = queue.popleft()
        
        # address_service_id, name, prefix, parent_name, _type
        query1 = """
            SELECT ad.id, ad.name, ad.prefix, ad1.name as parent_name, ad.type  
            FROM ghtk.address_service ad 
            LEFT JOIN ghtk.address_service ad1 on ad.parent_id = ad1.id
            WHERE ad.parent_id =""" + str(pair_address[1])  # BANG NAY CHUAN HON, 46767 ROWS
        address_1 = connect_db(cnx, CONFIG_DB, query1)
        
        if not address_1:
            num_continue += 1
            print("continue: ", num_continue)
            continue
        
        # Address_id, address_name, address_type, address_parent
        query2 = """
            SELECT ad.id, ad.name, ad.type, ad1.name as parent_name  
            FROM ghtk.addresses_filter ad 
            LEFT JOIN ghtk.addresses_filter ad1 on ad.parent_id = ad1.id
            WHERE ad.parent_id =""" + str(pair_address[0])   # BANG NAY CUA GHTK, 23484 ROWS
        address_2 = connect_db(cnx,CONFIG_DB, query2)
        
        for add_1 in address_1:
            temp_pairs = {}
            for add_2 in address_2:
                temp_wrong = [add_2[0], add_1[0]]
                if (add_1[4] != add_2[2] ):
                    continue
                full_name = str(add_1[2])+ " " + add_1[1]
                simillar = addr_similar(full_name, add_2[1])
                if( simillar > 0.5):
                    temp_pair = [add_2[0], add_1[0], add_2[1].rstrip(' \t\n\r'), add_1[1], add_2[2], add_1[2], add_2[3], add_1[3] ]
                    temp_pairs[simillar] = temp_pair
            if not temp_pairs:
                continue
            max_simillar = max(temp_pairs.keys())
            new_pair = temp_pairs[max_simillar]
            append_pair = [new_pair[0], new_pair[1] ]
            if (append_pair in wrong_addrs):
                print("wwwroooooonnnngggggg!!!!!!!!!")
                continue
            queue.append(append_pair)
            if(addr_similar(new_pair[2], new_pair[3])==1):
                new_pair.append("1")
            else:
                new_pair.append(round(max_simillar,3))
            
            if(append_pair in true_addrs):
                new_pair.append("1")
            elif(append_pair in notsure_addrs):
                new_pair.append("NOT SURE")
            else:
                new_pair.append("")


            mapping_result.append(new_pair)
            num_continue = 0
            print("new pair:", new_pair)
    
    print("Total: ", len(mapping_result))
    with open(FILE_MAP_OUT, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(mapping_result)

    csvFile.close()
    cnx.close()
        

start_time = time.time()
# main()
# a = addr_similar("Ecohome", "Ecohome Phúc Lợi")
# print(a)
elapsed_time = time.time() - start_time
print("\n------ Elapsed time: " + str(round(elapsed_time, 3)) + "s ------")



