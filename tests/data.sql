INSERT INTO users (username, email, password)
VALUES
    ('test', 'test@test.com', 'pbkdf2:sha256:150000$cjZ5YQsI$bba5883384d23c93a6b90d56f8dfb65b8c366f3e243040ead9ca48a0f5cc9f6a'),
    ('other', 'other@other.com', 'pbkdf2:sha256:150000$lynaUI7Z$9a5e1377b677c97c4e4b731e25fdcc3ec5dac8e23d09e8f7532f0bdc70e8c407');

INSERT INTO accounts (user_id, account, psswd_min, psswd_max, password, last_password, updated)
VALUES
    (1, 'Test_acc', 3, 5, '12345', '123', 1);
