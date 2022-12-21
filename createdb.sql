create table budget(
    codename varchar(255) primary key,
    daily_limit integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_expense, aliases)
values
    ("products", "продукти", true, "їжа"),
    ("coffee", "кава", true, ""),
    ("dinner", "обід", true, "ланч, бізнес-ланч, вечеря"),
    ("cafe", "кава", true, "ресторан, рест, макдональдс, kfc"),
    ("transport", "міськ. транспорт", false, "трамвай, тролейбус, автобус"),
    ("taxi", "таксі", false, "bolt, optima taxi"),
    ("phone", "телефон", false, "зв'язок"),
    ("books", "книги", false, "література"),
    ("internet", "інтернет", false, "inet"),
    ("other", "інші", true, "");

insert into budget(codename, daily_limit) values ('base', 8000);
