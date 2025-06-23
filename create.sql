use basefinancechat;

create table if not exists items (
    id int auto_increment primary key,
    item varchar(255) not null,
    qtd int not null,
    total decimal(10,2) not null,
    natureza varchar(50) not null,
    parcelado boolean not null,
    parcelas int,
    parcela_atual int, 
    valor_parcela_atual decimal(10,2) not null,
    date_create datetime not null default current_timestamp
);

create table if not exists users (
    id int auto_increment primary key,
    username varchar(255) not null,
    hashkey varchar(255) not null,
    date_create datetime not null default current_timestamp, 
    unique key unique_name_hashkey (username, hashkey),
    unique key unique_name (username)
);

insert into users (username, hashkey) values ('user', '8fb5cfe922674e0f9faa46a92716f66bd67ad344');
