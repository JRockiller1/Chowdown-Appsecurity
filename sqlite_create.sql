CREATE TABLE customer (
	cid integer PRIMARY KEY AUTOINCREMENT,
	cname varchar,
	cmail varchar,
	cmobile integer, 
	caddress varchar,
	cpassword varchar
);

CREATE TABLE restadmin (
	rid integer PRIMARY KEY AUTOINCREMENT,
	rname varchar,	
	rmail varchar,
	rmobile integer,
	raddress varchar,
	rpassword varchar,
	rstar varchar,
	rreview varchar
);

CREATE TABLE diginadmin (
	amail varchar,
	apassword varchar
);

CREATE TABLE items (
	iid integer,
	iname varchar,
	iprice integer,
	rid integer,
);

CREATE TABLE orders (
	oid integer,
	cid integer,
	rid integer,
	iid integer,
	payment text;
	month1 integer;
	rname text;
);

CREATE TABLE rating (
	rid integer,
	rstar varchar,
	rreview varchar
	
);


CREATE TABLE data (
	rid integer,
	month integer,
	year integer
);

CREATE TABLE promotion (
	key3 integer PRIMARY KEY AUTOINCREMENT,
	rid integer,
	promo text,
	discount integer
);

