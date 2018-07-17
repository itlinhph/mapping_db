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
