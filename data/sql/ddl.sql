CREATE TABLE IF NOT EXISTS products (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT    NULL,
    price       INTEGER NOT NULL,
    discount    INTEGER NOT NULL DEFAULT 0,
    reg_date    TEXT    NOT NULL
);

create table if not exists okinawa (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    zip_code TEXT    NOT NULL,
    zip_code_sub TEXT    NOT NULL,
    zip_code_ex TEXT    NOT NULL,
    addr1 TEXT    NOT NULL,
    addr2 TEXT    NOT NULL,
    addr3 TEXT    NOT NULL,
    addr4 TEXT    NOT NULL,
    addr5 TEXT    NOT NULL,
    addr6 TEXT    NOT NULL
);

create table if not exists text_file (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    line_no     INTEGER NOT NULL,
    path        TEXT NOT NULL,
    is_empty    INTEGER NOT NULL,
    line        TEXT NOT NULL
);
