import mysql.connector
import time
import csv

# Connect to DB report
CONFIG_DEV_GEARMAN = {
    'user': '******',
    'password': '******',
    'host': '******',
    'database': '******',
}

CONFIG_DB_REPORT = {
    'user': '******',
    'password': '******',
    'host': '******',
    'port' : '******',
    'database': '******',
}

FROMDATE = '2018-08-01'
TODATE   = '2018-08-20 17:55:00'
FEATURE_LIST = ['id ', 'name ', 'parent_id ', 'province_id ', 'type ', 'is_picked ', 'is_delivered ', 'created ', 'modified ']
FILE_OUT = 'update-changedb.csv'
def countdb(cnx):
    query = "select count(*) from ******.******"
    cursor = cnx.cursor()
    cursor.execute(query)
    (num_rows,) = cursor.fetchone()

    return num_rows

def fetch_new_data(cnx):
    query = """
    SELECT id, name, parent_id, province_id, type, is_picked, is_delivered, created, modified 
    FROM addresses 
    WHERE modified BETWEEN ' """ + FROMDATE + "' AND '" + TODATE + "' ORDER BY modified desc"

    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_db_address_old(cnx, address_id):
    query = "SELECT id, name, parent_id, province_id, type, is_picked, is_delivered, created, modified FROM ****** WHERE id =" + str(address_id)

    cursor = cnx.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    return row

def get_ads_mapping(cnx, id, name, parent_id, province_id):
    replace_list = ['phường ', 'xã ', 'thị trấn ', 'quận ', 'huyện ', 'đường ', 'phố ', 'thành phố ', 'thị xã ' ]
    name = name.lower()
    for item in replace_list:
        name = name.replace(item, "")
    query1 = "SELECT id, name, parent_id, province_id, prefix FROM ******.****** WHERE name like '" + name + "'" + "and parent_id = (select ****** from ****** where ****** =" + str(parent_id) + ")"
    cursor = cnx.cursor()
    cursor.execute(query1)
    row = cursor.fetchone()
    if row is None:
        query2 = "SELECT id, name, parent_id, province_id, prefix FROM ******.****** WHERE name like '" + name + "'" + "and province_id = (select ****** from ****** where ****** =" + str(province_id) + ")"
        cursor = cnx.cursor()
        cursor.execute(query2)
        row = list(cursor.fetchone())
        if row is None:
            row = ["SAI TT", "SAI TT", "SAI TT", "SAI TT", "SAI TT"]
        else:
            row.append("Sai District")
    else:
        row = list(row)
        query3 = "SELECT * FROM ******.****** where ****** = " + str(row[0])
        cursor = cnx.cursor()
        cursor.execute(query3)
        mapping = cursor.fetchone()
        if mapping is None:
            row.insert(0,"Chưa map")
            insert_query = "INSERT INTO ****** (`******`, `******`, `******`) VALUES ("+str(id) +"," + str(row[1]) +",1);"
            row.append(insert_query)
        else:
            row.insert(0,"Đã map")
    return row
    

def main():
    cnx_dev_gearman =  mysql.connector.connect(**CONFIG_DEV_GEARMAN)
    cnx_dbreport =  mysql.connector.connect(**CONFIG_DB_REPORT)

    # allrows = countdb(cnx_dev_gearman)
    newdata = fetch_new_data(cnx_dbreport)
    list_data_change = [['id ', 'name ', 'parent_id ', 'province_id ', 'type ', 'is_picked ', 'is_delivered ', 'created ', 'modified ', 'NOTE', 'OLD VALUE 1', 'OLD VALUE 2', 'Parent_id', 'Province_id']]
    for new_row in newdata:
        row_change = []
        db_address_old = get_db_address_old(cnx_dev_gearman, new_row[0])
        print(new_row)
        print(db_address_old)
        for item in new_row:
            row_change.append(item)
        if (db_address_old is None):
            db_map = get_ads_mapping(cnx_dev_gearman, new_row[0], new_row[1], new_row[2], new_row[3] )
            for item in db_map:
                row_change.append(item)
        else:
            index_change = []
            for i,feature in enumerate(db_address_old):
                # print(feature, db_address_old[i])
                if feature != new_row[i] and i !=8:
                    index_change.append(i)
            note = ""
            for index in index_change:
                note += FEATURE_LIST[index]
            print(note)

            row_change.append(note)
            for index in index_change:
                row_change.append(db_address_old[index])
            

        list_data_change.append(row_change)
        
    print("Total: ", len(list_data_change))
    with open(FILE_OUT, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(list_data_change)

    csvFile.close()
        


    cnx_dbreport.close()
    cnx_dev_gearman.close()

# start_time = time.time()
main()

# elapsed_time = time.time() - start_time
# print("\n Elapsed time: " + str(round(elapsed_time, 3)) + "s ")