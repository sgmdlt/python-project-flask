DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS urls_checks;

CREATE TABLE urls (
    id INTEGER NOT NULL, 
    name VARCHAR(255), 
    created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE urls_checks (
    id INTEGER NOT NULL, 
    url_id INTEGER, 
    status_code INTEGER, 
    h1 VARCHAR(255), 
    title VARCHAR(255), 
    description VARCHAR(255), 
    created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
    PRIMARY KEY (id), 
    FOREIGN KEY(url_id) REFERENCES urls (id) ON DELETE CASCADE ON UPDATE CASCADE
);