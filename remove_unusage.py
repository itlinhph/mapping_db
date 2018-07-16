import csv


def load_checked_data(file_name):
    list_pairs = []
    for line in open(file_name).readlines():
        line = line[:-1].split("\t")
        list_pairs.append(list(map(int, line)))
    
    return list_pairs


def filter_data():
    list_true_address = load_checked_data("data/true_addr.csv")
    print(len(list_true_address))

    list_id_address = open("data/addresses_id.csv").read().splitlines()
    list_id_address = list(map(int, list_id_address))
    print(len(list_id_address))

    filter_list = []
    for pairs in list_true_address:
        if pairs[0] in list_id_address:
            if not pairs in filter_list:
                filter_list.append(pairs)
    print(len(filter_list))
    with open("true_addr_filter.csv", 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(filter_list)


filter_data()
