CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_producto (
    id_amonet_producto UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    codigo VARCHAR(255) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    id_amonet_marca UUID NOT NULL,
    CONSTRAINT fk_marca
        FOREIGN KEY (id_amonet_marca)
        REFERENCES amonet_marca(id_amonet_marca)
        ON DELETE CASCADE
);

ALTER TABLE amonet_producto ADD COLUMN status BOOLEAN NOT NULL DEFAULT TRUE;
