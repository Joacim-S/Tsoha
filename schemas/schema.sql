CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    displayname TEXT, 
    password TEXT, 
    gender TEXT, 
    f_interest BOOLEAN, 
    m_interest BOOLEAN, 
    o_interest BOOLEAN, 
    dob DATE,
    visible BOOLEAN
);

CREATE TABLE things(
    id SERIAL PRIMARY KEY,
    item TEXT
);

CREATE TABLE likes(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    item_id INTEGER REFERENCES things,
    likes BOOLEAN
);

CREATE TABLE messages(
    id SERIAL PRIMARY KEY,
    content TEXT,
    sender_id INTEGER REFERENCES users,
    receiver_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE blocks(
    id SERIAL PRIMARY KEY,
    blocker_id INTEGER REFERENCES users,
    blocked_id INTEGER REFERENCES users
);

CREATE TABLE requests(
    id SERIAL PRIMARY KEY,
    content INTEGER,
    sender_id INTEGER REFERENCES users,
    receiver_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);