import csv
import mysql.connector

CONFIG_DB = {
    'user': 'linhph',
    'password': '',
    'host': 'localhost',
    'database': 'ghtk',
}

def load_checked_data(file_name):
    list_pairs = []
    for line in open(file_name).readlines():
        line = line[:-1].split("\t")
        list_pairs.append(list(map(int, line)))
    
    return list_pairs

def write_to_file(file_name, list_item):
    with open(file_name, 'w') as filehandle:
        for item in list_item:
            filehandle.write('%s\n' % item)
    
def connect_db(cnx, pairs):
    
    query = """
            SELECT ad.id, ad.name, ad.type, ad1.name as parent_name  
            FROM ghtk.addresses_filter ad 
            LEFT JOIN ghtk.addresses_filter ad1 on ad.parent_id = ad1.id
            WHERE ad.id= """ + str(pairs[0])
    cursor = cnx.cursor()
    cursor.execute(query)
    ad = cursor.fetchone()
    
    query = """
            SELECT ad.id, ad.name, ad.type, ad1.name as parent_name, ad.prefix 
            FROM ghtk.address_service ad 
            LEFT JOIN ghtk.address_service ad1 on ad.parent_id = ad1.id
            WHERE ad.id= """ + str(pairs[1])
    cursor = cnx.cursor()
    cursor.execute(query)
    ads = cursor.fetchone()
    print(pairs)
    print(ad)
    print(ads)
    if (ad is None):
        ad = (pairs[0], "EMPTY","EMPTY","EMPTY")
    if (ads is None):
        ads = (pairs[1], "EMPTY","EMPTY","EMPTY", "EMPTY")

    result = ad + ads

    
    return result

def convert_to_real_list(old_list):
    new_list = []
    for item in old_list:
        item = item.split("\t")
        new_list.append(item)
    return new_list

def combine_result(list_item, note):
    for item in list_item:
        item = 1
def main():

    linh_data = open("data_compare/linh.csv").read().splitlines()
    hien_data = open("data_compare/hien.csv").read().splitlines()

    common_list = list(set(linh_data).intersection(hien_data))
    linh_more = list(set(linh_data) - set(common_list))
    hien_more = list(set(hien_data) - set(common_list))

    print("Linh: ", len(linh_data))
    print("hien: ", len(hien_data))
    print("COMMON: ", len(common_list))

    write_to_file("data_compare/common_list.csv",common_list)
    write_to_file("data_compare/linh_more.csv", linh_more)
    write_to_file("data_compare/hien_more.csv", hien_more)

    common_list = convert_to_real_list(common_list)
    linh_more = convert_to_real_list(linh_more)
    hien_more = convert_to_real_list(hien_more)
    
    
    cnx = mysql.connector.connect(**CONFIG_DB)
    compare_result = []
    compare_result.append(["addr_id", "addr_service_id", "add_name", "addr_service_name", "addr_type", "addr_prefix", "addr_parent", "addrservice_parent", "NOTE"])
    
    for item in common_list:
        row = connect_db(cnx, item)
        new_row = [row[0], row[4], row[1].rstrip(' \t\n\r'), row[5], row[2], row[8], row[3], row[7], "COMMON" ]
        compare_result.append(new_row)
    
    for item in linh_more:
        row = connect_db(cnx, item)
        new_row = [row[0], row[4], row[1].rstrip(' \t\n\r'), row[5], row[2], row[8], row[3], row[7], "LINH" ]
        compare_result.append(new_row)
    
    for item in hien_more:
        row = connect_db(cnx, item)
        new_row = [row[0], row[4], row[1].rstrip(' \t\n\r'), row[5], row[2], row[8], row[3], row[7], "HIEN" ]
        compare_result.append(new_row)
    
    cnx.close()

    with open("compare_result.csv", 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(compare_result)


main()
