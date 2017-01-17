create table bluetooth (
  id int not null auto_increment,
  sensor_id int not null,
  mac_address char(17) not null,
  duration int DEFAULT null,
  date_time datetime not null,
  primary key (id)
);

create table wifi (
   id int  not null auto_increment,
   sensor_id int not null,
   mac_address char(17) not null,
   first_time datetime not null,
   last_time datetime not null,
   primary key (id)
);

create table sound (
   id int  not null auto_increment,
   sensor_id int not null,
   noise float not null,
   peak float not null,
   date_time datetime not null,
   primary key (id)
);
