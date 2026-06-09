CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE cat_amonet_tipo_materia_prima (
    id_cat_amonet_tipo_materia_prima UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL UNIQUE
);
