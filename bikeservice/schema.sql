DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS bike;
DROP TABLE IF EXISTS part;

CREATE TABLE user (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL
);

CREATE TABLE post (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      author_id INTEGER NOT NULL,
      created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      title TEXT NOT NULL,
      body TEXT NOT NULL,
      FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE bike(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    acquired DATE NOT NULL,
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    km REAL,
    FOREIGN KEY (owner_id) REFERENCES user (id)
);

CREATE TABLE part(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    bike_id INTEGER,
    acquired DATE NOT NULL,
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    part_type TEXT NOT NULL,
    dimensions TEXT,
    km REAL,
    FOREIGN KEY (owner_id) REFERENCES user (id)
    FOREIGN KEY (bike_id) REFERENCES bike (id)
);



CREATE TABLE bike_part(
    bike_id INTEGER NOT NULL,
    part_id INTEGER NOT NULL,
    km REAL,
    since DATE,
    FOREIGN KEY (bike_id) REFERENCES bike (id),
    FOREIGN KEY (part_id) REFERENCES part (id)
);

