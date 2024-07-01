-- Use the newly created database
USE familyPolicy;

DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS pdf_;
DROP TABLE IF EXISTS warranty;
DROP TABLE IF EXISTS insurance;
DROP TABLE IF EXISTS member;

create table member
(
	name nvarchar(20) not null,
	role nvarchar(20) not null,
	birthday date not null,
	primary key(name)
);

create table insurance
(
	company nvarchar(40) not null,
	product_name nvarchar(120) not null,
	product_type nvarchar(40) not null,
	coverage money not null check(coverage>0),
	duration tinyint not null check(duration>0),
	payment_time tinyint not null check(payment_time>0),
	primary key (company,product_name)
);
CREATE INDEX idx_product_type ON insurance(product_type);

create table warranty
(
warranty_number nchar(20) not null,
effective_date date not null,
premium money not null,
payment_state bit not null,
next_pay_day date,
period smallint, --ÔÂ·ÝÊý
state nvarchar(20) not null,
name nvarchar(20) not null,
product_name nvarchar(120) not null,
company nvarchar(40) not null,
primary key (warranty_number),
foreign key (name) references member on delete cascade,
foreign key (company, product_name) references insurance
);
CREATE INDEX idx_name ON warranty(name);
CREATE INDEX idx_company_product ON warranty(company, product_name);
CREATE INDEX idx_state ON warranty(state);

create table payment(
warranty_number nchar(20) not null,
pay_date date,
fee money,
tail_number nchar(4),
primary key (warranty_number, pay_date),
foreign key (warranty_number) references warranty
);
CREATE INDEX idx_pay_date ON payment(pay_date);

create table pdf_(
warranty_number nchar(20) not null,
pdf varbinary(max) not null,
primary key (warranty_number),
foreign key (warranty_number) references warranty
);

-- member
insert into member values('Zhang San','Male Lead','1978-11-13');
insert into member values('Li Si','Female Lead','1979-05-05');
insert into member values('Zhang Si','Son','2013-04-10');
insert into member values('Zhang Er','Grandfather','1950-09-10');
insert into member values('Wang Wu','Grandmother','1951-03-02');
insert into member values('Li San','Maternal Grandfather','1949-01-23');
insert into member values('Niu Yi','Maternal Grandmother','1951-10-06');

-- insurance
insert into insurance values('Pacific Life Insurance','Pacific Life Ankang Critical Illness Protection Plan' , 'Critical Illness Insurance', 500000, 30, 20); 
insert into insurance values('Hai Bao Life','Hai Bao Life Health Worry-free Critical Illness Insurance' , 'Critical Illness Insurance', 200000, 25, 20); 
insert into insurance values('Generali China Life','Generali Health Baby Children¡¯s Critical Illness Insurance' , 'Critical Illness Insurance', 400000, 25, 15); 
insert into insurance values('Zhong An Insurance','Zhong An Zunxiang e Sheng Million Medical Insurance' , 'Medical Insurance', 1000000, 1, 1); 
insert into insurance values('China Life','China Life Comprehensive Medical Insurance' , 'Medical Insurance', 500000, 1, 1); 
insert into insurance values('Hai Bao Life','Hai Bao Xin¡¯an Comprehensive Medical Insurance' , 'Medical Insurance', 600000, 1, 1); 
insert into insurance values('Ping An Life','Ping An Life Health Guardian Medical Insurance' , 'Medical Insurance', 700000, 1, 1); 
insert into insurance values('Zhong An Insurance','Zhong An Children¡¯s Vaccine Accident Insurance' , 'Accident Insurance', 300000, 1, 1); 
insert into insurance values('Ping An Life','Ping An Anxin Accident Insurance' , 'Accident Insurance', 400000, 1, 1); 
insert into insurance values('Manulife-Sinochem','Manulife-Sinochem Accident Protection Plan' , 'Accident Insurance', 500000, 1, 1); 
insert into insurance values('Ping An Life','Ping An Xiao Wantong Children¡¯s Accident Insurance' , 'Accident Insurance', 200000, 1, 1); 
insert into insurance values('Manulife-Sinochem','Manulife-Sinochem Lexiang Kangjian Critical Illness Insurance' , 'Critical Illness Insurance', 400000, 30, 20); 
insert into insurance values('Generali China Life','Generali Ankang Accident Insurance' , 'Accident Insurance', 250000, 1, 1); 
insert into insurance values('Hai Bao Life','Hai Bao Longevity Ankang Annuity Insurance' , 'Pension Insurance', 1000000, 30, 30); 
insert into insurance values('Pacific Life Insurance','Pacific Life Kangai Whole Life Insurance' , 'Whole Life Insurance', 800000, 255, 20); 
insert into insurance values('Zhong An Insurance','Zhong An Term Life Insurance' , 'Term Life Insurance', 500000, 20, 20); 
insert into insurance values('PICC Life','PICC Life Fushou Ankang Whole Life Insurance' , 'Whole Life Insurance', 600000, 255, 20); 
insert into insurance values('Ping An Life','Ping An Fu Whole Life Insurance' , 'Whole Life Insurance', 700000, 255, 20);

-- warranty

insert into warranty values(98374652718234950632, '2020-03-30', 10000, 0, '2025-03-30', 12, 'Active', 'Zhang San', 'Pacific Life Ankang Critical Illness Protection Plan', 'Pacific Life Insurance');
insert into warranty values(48392715603829471625, '2024-03-14', 5000, 1, null, null, 'Active', 'Zhang San', 'China Life Comprehensive Medical Insurance', 'China Life');
insert into warranty values(73819256403728461529, '2024-01-22', 7000, 1, null, null, 'Active', 'Zhang San', 'Ping An Anxin Accident Insurance', 'Ping An Life');
insert into warranty values(16538472905718362490, '2020-08-14', 15000, 0, '2024-08-14', 24, 'Active', 'Zhang San', 'Pacific Life Kangai Whole Life Insurance', 'Pacific Life Insurance');

insert into warranty values(82647195037284916253, '2024-05-08', 5000, 1, null, null, 'Active', 'Li Si', 'Hai Bao Xin¡¯an Comprehensive Medical Insurance', 'Hai Bao Life');
insert into warranty values(19037482657139482057, '2024-02-27', 7000, 1, null, null, 'Active', 'Li Si', 'Manulife-Sinochem Accident Protection Plan', 'Manulife-Sinochem');
insert into warranty values(37581249037628149502, '2021-07-08', 15000, 1, '2025-07-08', 12, 'Active', 'Li Si', 'Ping An Fu Whole Life Insurance', 'Ping An Life');

insert into warranty values(20487193652849301745, '2023-11-01', 2500, 0, '2024-11-01', 6, 'Active', 'Zhang Si', 'Generali Health Baby Children¡¯s Critical Illness Insurance', 'Generali China Life');
insert into warranty values(85917346205198432761, '2024-04-18', 3000, 1, null, null, 'Active', 'Zhang Si', 'Zhong An Children¡¯s Vaccine Accident Insurance', 'Zhong An Insurance');
insert into warranty values(29384715620839471635, '2024-05-15', 5000, 1, null, null, 'Active', 'Zhang Si', 'Ping An Xiao Wantong Children¡¯s Accident Insurance', 'Ping An Life');
insert into warranty values(91736420581943726504, '2024-01-17', 6000, 1, null, null, 'Active', 'Zhang Si', 'Zhong An Zunxiang e Sheng Million Medical Insurance', 'Zhong An Insurance');

insert into warranty values(47382951640738291560,'2022-03-15', 15000, 0, '2025-03-15', 12, 'Active', 'Zhang Er', 'Pacific Life Ankang Critical Illness Protection Plan', 'Pacific Life Insurance');
insert into warranty values(62819357492038471526, '2024-03-05', 5000, 1, null, null, 'Active', 'Zhang Er', 'China Life Comprehensive Medical Insurance', 'China Life');
insert into warranty values(50917362481509372648, '2024-04-01', 7000, 1, null, null, 'Active', 'Zhang Er', 'Manulife-Sinochem Accident Protection Plan', 'Manulife-Sinochem');
insert into warranty values(82736510482937501629, '2020-08-05', 15000, 1, '2025-08-05', 12, 'Active', 'Zhang Er', 'PICC Life Fushou Ankang Whole Life Insurance', 'PICC Life');

insert into warranty values(38291746502819374650, '2021-11-22', 15000, 0, '2024-11-22', 12, 'Active', 'Wang Wu', 'Pacific Life Ankang Critical Illness Protection Plan', 'Pacific Life Insurance');
insert into warranty values(10482736581902746538, '2024-02-11', 5000, 1, null, null, 'Active', 'Wang Wu', 'Hai Bao Xin¡¯an Comprehensive Medical Insurance', 'Hai Bao Life');
insert into warranty values(91736425810394726158, '2024-01-30', 7000, 1, null, null, 'Active', 'Wang Wu', 'Manulife-Sinochem Accident Protection Plan', 'Manulife-Sinochem');
insert into warranty values(56482917365048293715, '2024-03-11', 15000, 0, '2025-03-11', 12, 'Active', 'Wang Wu', 'Ping An Fu Whole Life Insurance', 'Ping An Life');

insert into warranty values(73498162509374816259, '2023-02-14', 15000, 0, '2025-02-14', 12, 'Active', 'Li San', 'Pacific Life Ankang Critical Illness Protection Plan', 'Pacific Life Insurance');
insert into warranty values(21987405618392740562, '2024-05-03', 5000, 1, null, null, 'Active', 'Li San', 'Hai Bao Xin¡¯an Comprehensive Medical Insurance', 'Hai Bao Life');
insert into warranty values(86529471038294715603, '2024-03-21', 7000, 1, null, null, 'Active', 'Li San', 'Manulife-Sinochem Accident Protection Plan', 'Manulife-Sinochem');
insert into warranty values(17048239651728394605, '2022-10-03', 15000, 0, '2024-10-03', 12, 'Active', 'Li San', 'PICC Life Fushou Ankang Whole Life Insurance', 'PICC Life');

insert into warranty values(35817492057183942658, '2021-05-11', 15000, 0, '2025-05-11', 12, 'Active', 'Niu Yi', 'Pacific Life Ankang Critical Illness Protection Plan', 'Pacific Life Insurance');
insert into warranty values(49271635810294738561, '2024-04-26', 5000, 1, null, null, 'Active', 'Niu Yi', 'Hai Bao Xin¡¯an Comprehensive Medical Insurance', 'Hai Bao Life');
insert into warranty values(63748219503827461529, '2024-02-09', 7000, 1, null, null, 'Active', 'Niu Yi', 'Manulife-Sinochem Accident Protection Plan', 'Manulife-Sinochem');
insert into warranty values(58294071658392741506, '2020-12-30', 15000, 0, '2024-12-30', 12, 'Active', 'Niu Yi', 'Ping An Fu Whole Life Insurance', 'Ping An Life');


-- payment

insert into payment values(98374652718234950632, '2020-03-30', 10000, 2901);
insert into payment values(98374652718234950632, '2021-03-20', 10000, 2901);
insert into payment values(98374652718234950632, '2022-03-09', 10000, 1062);
insert into payment values(98374652718234950632, '2023-03-21', 10000, 1062);
insert into payment values(98374652718234950632, '2024-03-21', 10000, 1062);
insert into payment values(48392715603829471625, '2024-04-18', 5000, 1062);
insert into payment values(73819256403728461529, '2024-05-15', 7000, 2932);
insert into payment values(16538472905718362490, '2020-08-14', 15000, 2901);
insert into payment values(16538472905718362490, '2021-08-01', 15000, 2901);
insert into payment values(16538472905718362490, '2022-08-09', 15000, 1062);
insert into payment values(16538472905718362490, '2023-08-10', 15000, 1062);

insert into payment values(82647195037284916253, '2024-05-08', 5000, 2932);
insert into payment values(19037482657139482057, '2024-02-27', 7000, 1062);
insert into payment values(37581249037628149502, '2021-07-08', 15000, 2901);
insert into payment values(37581249037628149502, '2022-07-06', 15000, 2901);
insert into payment values(37581249037628149502, '2023-07-01', 15000, 1062);
insert into payment values(37581249037628149502, '2024-05-29', 15000, 1062);

insert into payment values(20487193652849301745, '2023-11-01', 2500, 1062);
insert into payment values(20487193652849301745, '2024-05-01', 2500, 1062);
insert into payment values(85917346205198432761, '2024-04-18', 3000, 1062);
insert into payment values(29384715620839471635, '2024-05-15', 5000, 1062);
insert into payment values(91736420581943726504, '2024-01-17', 6000, 1062);

insert into payment values(47382951640738291560, '2022-03-15', 15000, 2901);
insert into payment values(47382951640738291560, '2023-03-10', 15000, 1062);
insert into payment values(47382951640738291560, '2024-03-01', 15000, 2932);
insert into payment values(62819357492038471526, '2024-03-05', 5000, 2932);
insert into payment values(50917362481509372648, '2024-04-01', 7000, 1062);
insert into payment values(82736510482937501629, '2020-08-05', 15000, 2901);
insert into payment values(82736510482937501629, '2021-08-01', 15000, 2901);
insert into payment values(82736510482937501629, '2022-08-05', 15000, 2901);
insert into payment values(82736510482937501629, '2023-08-04', 15000, 1062);
insert into payment values(82736510482937501629, '2024-05-29', 15000, 1062);

insert into payment values(38291746502819374650, '2021-11-22', 15000, 2901);
insert into payment values(38291746502819374650, '2022-11-10', 15000, 1062);
insert into payment values(38291746502819374650, '2023-11-21', 15000, 1062);
insert into payment values(10482736581902746538, '2024-02-11', 5000, 1062);
insert into payment values(91736425810394726158, '2024-01-30', 7000, 1062);
insert into payment values(56482917365048293715, '2024-03-11', 15000, 1062);

insert into payment values(73498162509374816259, '2023-02-14', 15000, 1062);
insert into payment values(73498162509374816259, '2024-02-10', 15000, 1062);
insert into payment values(21987405618392740562, '2024-05-03', 5000, 1062);
insert into payment values(86529471038294715603, '2024-03-21', 7000, 1062);
insert into payment values(17048239651728394605, '2022-10-03', 15000, 1062);
insert into payment values(17048239651728394605, '2023-10-01', 15000, 1062);

insert into payment values(35817492057183942658, '2021-05-11', 15000, 2901);
insert into payment values(35817492057183942658, '2022-05-10', 15000, 2901);
insert into payment values(35817492057183942658, '2023-05-02', 15000, 2901);
insert into payment values(35817492057183942658, '2024-05-03', 15000, 1062);
insert into payment values(49271635810294738561, '2024-04-26', 5000, 1062);
insert into payment values(63748219503827461529, '2024-02-09', 7000, 1062);
insert into payment values(58294071658392741506, '2020-12-30', 15000, 2901);
insert into payment values(58294071658392741506, '2021-12-29', 15000, 2901);
insert into payment values(58294071658392741506, '2022-12-20', 15000, 2901);
insert into payment values(58294071658392741506, '2023-12-19', 15000, 1062);
