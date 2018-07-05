#!/usr/bin/python
# -*- coding: utf-8 -*-

# --- LINH PHAN ---
import csv
import mysql.connector
from difflib import SequenceMatcher
from collections import deque

# DB FULL:
DB_HOST1             = "localhost"
USERNAME1            = "root"
PASSWORD1            = ""
DB_NAME1             = "ghtk"
# QUERY_GETDB1         = "Select * from address_service limit 10"

# DB DEV_TUAN
DB_HOST2             = "10.6.0.1"
USERNAME2            = "linhph"
PASSWORD2            = "acf5f498c914e8fea7dec29219a1e4fc"
DB_NAME2             = "dev_tuannn"
# QUERY_GETDB2         = "Select * from addresses limit 10"

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
MAP_PROVINCE        = "map_province.txt"


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def connect_db(config_db,  query):
    # Connect database:
    cnx = mysql.connector.connect(**config_db)

    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cnx.close()
    return result


if __name__ == '__main__':

    mapping_result = []
    pairs = [l.split() for l in open(MAP_PROVINCE).readlines()]
    queue = deque(pairs)
    while (len(queue) != 0):
        pair_address = queue.popleft()
        mapping_result.append(pair_address)
        
        query1 = "Select id, name From address_service Where parent_id =" + pair_address[0]
        address_1 = connect_db(CONFIG_DB_FULL, query1)
        query2 = "Select id, name From addresses Where parent_id =" + pair_address[2]
        address_2 = connect_db(CONFIG_DB_DEVTUAN, query2)

        for add_1 in address_1:
            for add_2 in address_2:
                if(similar(add_1[1], add_2[1]) > 0.8):
                    new_pair = [add_1[0], add_2[0]]
                    queue.append(new_pair)
    
    for pair_add in mapping_result:
        print(pair_add)
        
    # queue.append("Terry")
    # queue.popleft()

    # add_full = connect_db(DB_HOST1, USERNAME1, PASSWORD1, DB_NAME1, QUERY_GETDB1)
    # add_tuandb = connect_db(DB_HOST2, USERNAME2, PASSWORD2, DB_NAME2, QUERY_GETDB2)

    # dict_add_full = {}
    # dict_add_tuandb = {}

    # for row in add_full:
    #     dict_add_full[row[0]] = row[1]

    # a= similar("bà huyện thanh quan", "bà thanh quan" )
    # print(a)

    # for row in add_tuandb:
    #     print row


