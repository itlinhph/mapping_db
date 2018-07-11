a = "Anh Lĩnh Có VẤN ĐÊ"
a = a.lower()
# a = convert_non_accented(a)
print(a)

# SELECT ad.id, ad.name, ad.type, ad1.name as parent_name  
#             FROM ghtk.addresses ad 
#             LEFT JOIN ghtk.addresses ad1 on ad.parent_id = ad1.id
#             WHERE ad.parent_id = (SELECT ad.parent_id  
# 									FROM ghtk.addresses ad 
# 									LEFT JOIN ghtk.addresses ad1 on ad.parent_id = ad1.id
# 									WHERE ad.id = 20723)
# 			AND ad.type = 1