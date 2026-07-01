CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_marca (
    id_amonet_marca UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL UNIQUE
);

ALTER TABLE amonet_marca ADD COLUMN status BOOLEAN NOT NULL DEFAULT TRUE;