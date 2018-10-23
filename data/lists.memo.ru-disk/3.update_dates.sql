update persons
 set BIRTHDATE_STR = case when BIRTHDATE > 0 then
concat(
if(BIRTHDATE & 31 > 0, concat(lpad( BIRTHDATE & 31,2,'0'),'.'),''),
if((BIRTHDATE >> 5) & 15 > 0, concat(lpad( (BIRTHDATE >> 5) & 15,2,'0'),'.'),''),
if((BIRTHDATE >> 9) & 255 > 0, ((BIRTHDATE >> 9) & 255) + 1800,'')
) 
else null end,
MORTDATE_STR = case when MORTDATE > 0 then
concat(
if(MORTDATE & 31 > 0, concat(lpad( MORTDATE & 31,2,'0'),'.'),''),
if((MORTDATE >> 5) & 15 > 0, concat(lpad( (MORTDATE >> 5) & 15,2,'0'),'.'),''),
if((MORTDATE >> 9) & 255 > 0, ((MORTDATE >> 9) & 255) + 1800,'')
) 
else null end,
ARESTDATE_STR = case when ARESTDATE > 0 then
concat(
if(ARESTDATE & 31 > 0, concat(lpad( ARESTDATE & 31,2,'0'),'.'),''),
if((ARESTDATE >> 5) & 15 > 0, concat(lpad( (ARESTDATE >> 5) & 15,2,'0'),'.'),''),
if((ARESTDATE >> 9) & 255 > 0, ((ARESTDATE >> 9) & 255) + 1800,'')
) 
else null end,
SUDDATE_STR = case when SUDDATE > 0 then
concat(
if(SUDDATE & 31 > 0, concat(lpad( SUDDATE & 31,2,'0'),'.'),''),
if((SUDDATE >> 5) & 15 > 0, concat(lpad( (SUDDATE >> 5) & 15,2,'0'),'.'),''),
if((SUDDATE >> 9) & 255 > 0, ((SUDDATE >> 9) & 255) + 1800,'')
) 
else null end,
REABDATE_STR = case when REABDATE > 0 then
concat(
if(REABDATE & 31 > 0, concat(lpad( REABDATE & 31,2,'0'),'.'),''),
if((REABDATE >> 5) & 15 > 0, concat(lpad( (REABDATE >> 5) & 15,2,'0'),'.'),''),
if((REABDATE >> 9) & 255 > 0, ((REABDATE >> 9) & 255) + 1800,'')
) 
else null end;

