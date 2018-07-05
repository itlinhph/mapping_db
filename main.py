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

# FILE MAPPING PROVINCE:
MAP_PROVINCE        = "map_province.txt"


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def connect_db(HOST, USER, PASSWD, DB,  QR):
    # Connect database:
    cnx = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, db=DB)

    cursor = cnx.cursor()
    cursor.execute(QR)
    result = cursor.fetchall()
    return result


if __name__ == '__main__':

    pairs = [l.split() for l in open(MAP_PROVINCE).readlines()]
    queue = deque(pairs)
    while (len(queue) != 0):
        print(queue.popleft())
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

