CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE cat_amonet_estado_produccion (
    id_cat_amonet_estado_produccion UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL UNIQUE
);
