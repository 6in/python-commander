create database if not exists `praqta-dev` 
	default character set utf8 
	collate utf8_general_ci;

create table if not exists okinawa (
	id		SERIAL primary key,
	zip_code	TEXT NOT NULL,
	zip_code_sub	TEXT NOT NULL,
	zip_code_ex	TEXT NOT NULL,
	addr1		TEXT NOT NULL,
	addr2		TEXT NOT NULL,
	addr3		TEXT NOT NULL,
	addr4		TEXT NOT NULL,
	addr5		TEXT NOT NULL,
	addr6		TEXT NOT NULL
);
