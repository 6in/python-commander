create table if not exists okinawa (
    id          SERIAL,
    zip_code TEXT    NOT NULL,
    zip_code_sub TEXT    NOT NULL,
    zip_code_ex TEXT    NOT NULL,
    addr1 TEXT    NOT NULL,
    addr2 TEXT    NOT NULL,
    addr3 TEXT    NOT NULL,
    addr4 TEXT    NOT NULL,
    addr5 TEXT    NOT NULL,
    addr6 TEXT    NOT NULL
)