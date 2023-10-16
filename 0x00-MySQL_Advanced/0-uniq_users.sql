-- 0 - create a user table
-- creates a table named user with id (pk, int), email(string), name
create table if not exists user (id int primary key not null auto_increment,
email varchar(255) not null unique, name varchar(255))
