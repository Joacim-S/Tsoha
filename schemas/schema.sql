CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, displayname TEXT, password TEXT, 
gender TEXT, interested_in TEXT, dob TEXT);