CREATE TABLE IF NOT EXISTS todos
(
    id          TEXT PRIMARY KEY,
    title       TEXT,
    description TEXT,
    is_done     BOOLEAN,
    created_at  TEXT,
    updated_at  TEXT
);
