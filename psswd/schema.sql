DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS accounts;


CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);


CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    account TEXT NOT NULL,
    psswd_min INTEGER NOT NULL,
    psswd_max INTEGER NOT NULL,
    password TEXT NOT NULL,
    last_password TEXT NOT NULL,
    updated INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
