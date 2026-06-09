CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE cat_amonet_tipo_unidad (
    id_cat_amonet_tipo_unidad UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,
    abreviacion VARCHAR(20) NOT NULL,
    UNIQUE (nombre, abreviacion)
);
