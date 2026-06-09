CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_producto_materia_prima (
    id_amonet_producto_materia_prima UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_amonet_producto UUID NOT NULL,
    id_amonet_materia_prima UUID NOT NULL,
    formula TEXT,
    CONSTRAINT fk_producto
        FOREIGN KEY (id_amonet_producto)
        REFERENCES amonet_producto(id_amonet_producto)
        ON DELETE CASCADE,
    CONSTRAINT fk_materia_prima
        FOREIGN KEY (id_amonet_materia_prima)
        REFERENCES amonet_materia_prima(id_amonet_materia_prima)
        ON DELETE CASCADE,
    CONSTRAINT uq_producto_materia_prima UNIQUE (id_amonet_producto, id_amonet_materia_prima)
);
