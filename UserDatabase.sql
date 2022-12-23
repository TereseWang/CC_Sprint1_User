drop database if exists user_database;
create database user_database;
use user_database;
create table user_info
(
    uid int auto_increment
        primary key,
    last_name   varchar(128) not null,
    first_name  varchar(128) not null,
    middle_name varchar(128) null,
    phone    varchar(256) not null,
    email       varchar(256) not null,
    pwd    varchar(256) not null,
    constraint user_info_email_uindex
        unique (email)
);