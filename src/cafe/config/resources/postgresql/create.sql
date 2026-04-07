-- Copyright (C) 2022 - present Juergen Zimmermann, Hochschule Karlsruhe
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.

-- TEXT statt varchar(n):
-- "There is no performance difference among these three types, apart from a few extra CPU cycles
-- to check the length when storing into a length-constrained column"
-- ggf. CHECK(char_length(nachname) <= 255)

-- https://www.postgresql.org/docs/current/manage-ag-tablespaces.html
SET default_tablespace = cafespace;

-- https://www.postgresql.org/docs/current/sql-createtable.html
-- https://www.postgresql.org/docs/current/datatype.html
-- https://www.postgresql.org/docs/current/sql-createtype.html
-- https://www.postgresql.org/docs/current/datatype-enum.html
CREATE TYPE kaffeesorte AS ENUM ('ESPRESSO','CAPPUCCINO','LATTE_MACCHIATO','AMERICANO','FLAT_WHITE','COLD_BREW','MATCHA'
);

-- TABELLE CAFE
CREATE TABLE IF NOT EXISTS cafe (
    id            INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    version       INTEGER NOT NULL DEFAULT 0,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    kategorie     INTEGER NOT NULL CHECK (kategorie >= 1 AND kategorie <= 9),
    gruendungsdatum DATE NOT NULL,
    kaffeesorten  JSONB,
    erzeugt       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    aktualisiert  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS cafe_name_idx ON cafe(name);

-- TABELLE CAFE_MANAGER
CREATE TABLE IF NOT EXISTS cafe_manager (
    id        INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    vorname   TEXT NOT NULL,
    nachname  TEXT NOT NULL,
    cafe_id   INTEGER NOT NULL REFERENCES cafe ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS cafe_manager_cafe_id_idx ON cafe_manager(cafe_id);

-- TABELLE PRODUKT
CREATE TABLE IF NOT EXISTS produkt (
    id        INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    name      TEXT NOT NULL,
    preis     NUMERIC(10,2) NOT NULL,
    waehrung  TEXT NOT NULL CHECK (waehrung ~ '[A-Z]{3}'),
    cafe_id   INTEGER NOT NULL REFERENCES cafe ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS produkt_cafe_id_idx ON produkt(cafe_id);
