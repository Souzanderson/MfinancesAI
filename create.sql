use basefinancechat;

create table items (
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