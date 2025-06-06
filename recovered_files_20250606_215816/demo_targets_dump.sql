PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM targets;
DELETE FROM operations;
DELETE FROM extracted_data;

INSERT INTO targets VALUES(1,'alx.trading','ALX Trading','https://example.com/alx.jpg',10000,500,100,1,0,'Leading trading insights','https://alxtrading.com','business',1,'active','2025-06-05 15:55:00','2025-06-05 15:55:00',NULL,'High priority target');
INSERT INTO targets VALUES(2,'whatilove1728','What I Love','https://example.com/whatilove.jpg',5000,300,50,1,0,'Sharing what I love','https://whatilove.com','personal',2,'active','2025-06-05 15:55:00','2025-06-05 15:55:00',NULL,'Secondary target');
COMMIT;