-- 1. Создаем саму таблицу
CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50),
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER
);

-- 2. Создаем таблицу групп
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 3. Связываем их
ALTER TABLE contacts 
    ADD CONSTRAINT fk_group 
    FOREIGN KEY (group_id) REFERENCES groups(id);

-- 4. Создаем таблицу телефонов
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20)  NOT NULL,
    type       VARCHAR(10)  CHECK (type IN ('home', 'work', 'mobile'))
);