CREATE TABLE {{schema}}.app_info (
    "key" VARCHAR NOT NULL PRIMARY KEY,
    "value" JSONB
);

-- For text indices
CREATE EXTENSION IF NOT EXISTS pg_trgm;