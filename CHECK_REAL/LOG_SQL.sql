-- AN GIANG
UPDATE `ghtk`.`address_service` SET `prefix`='Thành phố' WHERE `id`='452';
UPDATE `ghtk`.`address_service` SET `name`='Ô Long Vỹ' WHERE `id`='7071';
UPDATE `ghtk`.`address_service` SET `prefix`='Phường' WHERE `id`='7059';
-- Đổi Long Thành --> Thị Trấn Phú Mỹ
UPDATE `ghtk`.`address_service` SET `name`='Phú Mỹ', `prefix`='Thị Xã' WHERE `id`='207';
UPDATE `ghtk`.`address_service` SET `prefix`='Thành phố' WHERE `id`='202';
UPDATE `ghtk`.`address_service` SET `prefix`='Thị Trấn' WHERE `id`='2862';
UPDATE `ghtk`.`address_service` SET `prefix`='Phường' WHERE `id`='2870';
UPDATE `ghtk`.`address_service` SET `prefix`='Phường' WHERE `id`='2868';
UPDATE `ghtk`.`address_service` SET `prefix`='Phường' WHERE `id`='2869';
UPDATE `ghtk`.`address_service` SET `prefix`='Phường' WHERE `id`='2871';
-- Không có địa chỉ này
DELETE FROM `ghtk`.`address_service` WHERE `id`='2872';



-- BÀ RỊA VŨNG TÀU

-- Thị xã Phước Bửu
UPDATE `ghtk`.`address_service` SET `prefix`='Thị Trấn' WHERE `id`='2904';
-- Thành phố bà rịa
UPDATE `ghtk`.`address_service` SET `prefix`='Thành Phố' WHERE `id`='202';

-- Đổi tên phường 6 --> phường Thắng Nhì
DELETE FROM `ghtk`.`address_service` WHERE `id`='2886';

-- Thành lập thị xã giá rai từ huyện giá rai 2015
UPDATE `ghtk`.`address_service` SET `prefix`='Thị xã' WHERE `id`='691';











UPDATE `dev_gearman`.`district` SET `_prefix`='Thành phố' WHERE `id`='699';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thành phố' WHERE `id`='690';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thành phố' WHERE `id`='659';
UPDATE `dev_gearman`.`district` SET `_name`='Nà Hang' WHERE `id`='645';
UPDATE `dev_gearman`.`district` SET `_name`='Mù Căng Chải' WHERE `id`='634';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thị xã' WHERE `id`='628';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thị xã' WHERE `id`='609';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thị xã' WHERE `id`='603';
UPDATE `dev_gearman`.`district` SET `_name`='Cồn Cỏ' WHERE `id`='591';
UPDATE `dev_gearman`.`district` SET `_name`='Đắk Hà' WHERE `id`='572';
UPDATE `dev_gearman`.`district` SET `_name`='Đắk Tô' WHERE `id`='573';
UPDATE `dev_gearman`.`district` SET `_name`='Kon Tum' WHERE `id`='577';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thị xã' WHERE `id`='566';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thành phố' WHERE `id`='555';
UPDATE `dev_gearman`.`district` SET `_name`='Cao Lãnh' WHERE `id`='551';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thành phố' WHERE `id`='498';
UPDATE `dev_gearman`.`district` SET `_prefix`='Huyện' WHERE `id`='486';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thị xã' WHERE `id`='485';
UPDATE `dev_gearman`.`district` SET `_name`='Si Ma Cai' WHERE `id`='434';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thành phố' WHERE `id`='423';
UPDATE `dev_gearman`.`district` SET `_prefix`='Thị xã' WHERE `id`='420';
-- UPDATE `dev_gearman`.`district` SET `_prefix`='Thị xã' WHERE `id`='543';




UPDATE `dev_gearman`.`district` SET `_prefix`='Thành phố' WHERE `id`='415';
