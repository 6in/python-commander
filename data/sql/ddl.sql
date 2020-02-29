CREATE TABLE IF NOT EXISTS products (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT    NULL,
    price       INTEGER NOT NULL,
    discount    INTEGER NOT NULL DEFAULT 0,
    reg_date    TEXT    NOT NULL
);

