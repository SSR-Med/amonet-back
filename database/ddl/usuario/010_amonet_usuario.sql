CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_usuario (
    id_amonet_usuario UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    documento VARCHAR(40) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    rol VARCHAR(100) NOT NULL DEFAULT 'OPERARIO',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    password VARCHAR(255) NOT NULL
);
