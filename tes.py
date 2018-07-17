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




# GET ALL DATA CHECK BY PROVINCE ID
# SELECT ad.id, ad.name, ad.type, ad.prefix, ad1.id as parent_id, ad1.name as parent_name , ad1.province_id, ad.modified  
#             FROM ghtk.address_service ad 
#             LEFT JOIN ghtk.address_service ad1 on ad.parent_id = ad1.id
#             where ad.province_id in (30,10,55,37,25,4,23,13,39,12,3,11,38,5,47,22,53,6,16,49,14,8,43,44,9,36,48,32,1,26,52,40)
           