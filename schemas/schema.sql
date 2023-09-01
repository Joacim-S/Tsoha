CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, displayname TEXT, password TEXT, 
gender TEXT, f_interest BOOLEAN, m_interest BOOLEAN, o_interest BOOLEAN, dob DATE);