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
    unique key unique_name_hashkey (username, hashkey)
);

insert into users (username, hashkey) values ('anderson', '37664a95918e6e6640cec08ac708b5d91b456f63');
