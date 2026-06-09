CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_materia_prima (
    id_amonet_materia_prima UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL UNIQUE,
    id_cat_amonet_tipo_materia_prima UUID NOT NULL,
    id_cat_amonet_tipo_unidad UUID NOT NULL,
    CONSTRAINT fk_tipo_materia_prima
        FOREIGN KEY (id_cat_amonet_tipo_materia_prima)
        REFERENCES cat_amonet_tipo_materia_prima(id_cat_amonet_tipo_materia_prima)
        ON DELETE CASCADE,
    CONSTRAINT fk_tipo_unidad
        FOREIGN KEY (id_cat_amonet_tipo_unidad)
        REFERENCES cat_amonet_tipo_unidad(id_cat_amonet_tipo_unidad)
        ON DELETE CASCADE
);
