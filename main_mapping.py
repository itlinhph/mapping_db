#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Author: LinhPH 
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
FILE_MAP_OUT        = "mapping_as2507.csv"


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
    'phố ' : 'p '
}

def convert_non_accented(text):
    
    output = text

    for key, value in PREFIX.items():
        output = output.replace(key, value)
    for regex, replace in PATTERNS.items():
        output = re.sub(regex, replace, output)
    return output

def addr_similar(a, b):
    a = convert_non_accented(a)
    a = " ".join(a.split())
    b = convert_non_accented(b)
    b = " ".join(b.split())
    simillars = SequenceMatcher(None, a, b).ratio()
    print("String process: ", a,b, simillars)
    return simillars

def connect_db(cnx, query):
    
    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result


def load_checked_data(file_name):
    list_pairs = []
    for line in open(file_name).readlines():
        line = line[:-1].split("\t")
        list_pairs.append(list(map(int, line)))
    
    return list_pairs

# def get_parentid_remove_street(cnx):
#     query = "SELECT distinct(parent_id) FROM ghtk.clone_addresses WHERE type in (2,4,5,6)"
    

def main():
    cnx = mysql.connector.connect(**CONFIG_DB)
    mapping_result = []
    for line in open(MAP_ALL_PROVINCE).readlines():
        line = line[:-1].split(",")
        mapping_result.append(line)

    pairs = [l.split() for l in open(PAIR_PROVINCE).readlines()]
    # wrong_addrs = load_checked_data(WRONG_ADDRESSES)
    # true_addrs = load_checked_data(TRUE_ADDRESSES)
    # notsure_addrs = load_checked_data(NOTSURE_ADDRESSES)

    query = "SELECT distinct(parent_id) FROM ghtk.clone_addresses WHERE type in (2,4,5,6)"
    result = connect_db(cnx, query)
    list_parent_ward_min = []
    for item in result:
        list_parent_ward_min.append(item[0]) 
    print("List_parent: ",list_parent_ward_min)
    # return
    queue = deque(pairs)
    num_continue = 0
    while (len(queue) != 0 and num_continue < 40):
        pair_address = queue.popleft()
        
        # address_service_id, name, prefix, parent_name, _type
        query1 = """
            SELECT ad.id, ad.name, ad.prefix, ad1.name as parent_name, ad.type  
            FROM ghtk.address_service ad 
            LEFT JOIN ghtk.address_service ad1 on ad.parent_id = ad1.id
            WHERE ad.parent_id =""" + str(pair_address[1])  # BANG NAY CHUAN HON, 46530 ROWS
        address_1 = connect_db(cnx, query1)
        
        if not address_1:
            num_continue += 1
            print("continue: ", num_continue)
            continue
        
        # Address_id, address_name, address_type, pid, address_parent
        query2 = """
            SELECT ad.id, ad.name, ad.type, ad.parent_id, ad1.name as parent_name  
            FROM ghtk.clone_addresses ad 
            LEFT JOIN ghtk.clone_addresses ad1 on ad.parent_id = ad1.id
            WHERE ad.parent_id =""" + str(pair_address[0])   # BANG NAY CUA GHTK, 16779 ROWS
        address_2 = connect_db(cnx, query2)
        
        b_mapped = []
        as_not_map = []
        if(pair_address[0] in list_parent_ward_min):
            # print("remove_type_2", pair_address[0])
            remove_type_2 = False
            # print(pair_address[0])
        else:
            remove_type_2 = True
        
        for add_1 in address_1:
            as_id, as_name, as_prefix, as_pname, as_type = add_1
            
            if(remove_type_2 and as_type in (2,4,5,6)):
                # print("continue", pair_address[0], as_type, remove_type_2)
                continue
            if(as_type ==7):
                as_type_fix = 3
            elif(as_type in (4,5,6)):
                as_type_fix = 4
            else:
                as_type_fix = as_type
            max_simmilar = 0
            id_max = 0
            new_output = []
            for add_2 in address_2:
                b_id, b_name, b_type, b_pid, b_pname = add_2
                if(b_type ==7):
                    b_type_fix = 3
                elif(b_type in (4,5,6)):
                    b_type_fix = 4
                else:
                    b_type_fix = b_type

                if (as_type_fix != b_type_fix or max_simmilar >1):
                    continue
                # print(add_1)
                as_full_name = str(add_1[2]) + " " + add_1[1]
                as_full_name = as_full_name.lower()
                b_name_lower = b_name.lower()
                if(as_full_name == b_name_lower or as_name.lower() == b_name_lower):
                    new_output = [b_id, as_id, b_name, as_name, as_prefix, b_type, b_pid, b_pname, as_pname, "1"]
                    max_simmilar = 2
                elif( as_name.lower() in b_name_lower and len(as_name) > 2 ):
                    new_output = [b_id, as_id, b_name, as_name, as_prefix, b_type, b_pid, b_pname, as_pname, "Substring"]
                    max_simmilar = 0.8
                else:
                    simillar = addr_similar(as_full_name, b_name_lower)
                    if(simillar > max_simmilar):
                        new_output = [b_id, as_id, b_name, as_name, as_prefix, b_type, b_pid, b_pname, as_pname, round(simillar,3)]
                        max_simmilar = simillar
                        id_max = b_id
            
            if(max_simmilar >=0.7):
                mapping_result.append(new_output)
                queue.append( [new_output[0], new_output[1]] )
                b_mapped.append((new_output[0], new_output[2], new_output[5],new_output[6], new_output[7]))
                print("new: ", new_output)
                num_continue = 0
            
            else:
                as_alone = ["", as_id, "", as_name, as_prefix, as_type, "", "", as_pname, "A" ]
                as_not_map.append(as_alone)
        
        # print(address_2)
        # print(b_mapped)
        for item in as_not_map:
            mapping_result.append(item)
        for item in address_2:
            if item not in b_mapped:
                b_alone = [item[0], "", item[1], "", "", item[2], item[3], item[4], "", "Not-as"]
                mapping_result.append(b_alone)
        mapping_result.append(["","","","","","","","","",""])
      

    print("Total: ", len(mapping_result))
    with open(FILE_MAP_OUT, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(mapping_result)

    csvFile.close()
    cnx.close()
        

start_time = time.time()
# main()
a = addr_similar("dac glei", "dac glay")
print(a)


elapsed_time = time.time() - start_time
print("\n Elapsed time: " + str(round(elapsed_time, 3)) + "s ")




