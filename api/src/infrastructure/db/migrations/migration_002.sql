CREATE TABLE {{schema}}.measure (
    measure_id VARCHAR NOT NULL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    voltage FLOAT NOT NULL
);