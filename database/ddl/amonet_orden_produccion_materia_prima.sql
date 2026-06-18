CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_orden_produccion_materia_prima (
    id_amonet_orden_produccion_materia_prima UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    amonet_materia_prima_id UUID NOT NULL,
    amonet_orden_produccion_id UUID NOT NULL,
    CONSTRAINT fk_orden_prod_mat_prima_materia
        FOREIGN KEY (amonet_materia_prima_id)
        REFERENCES amonet_materia_prima(id_amonet_materia_prima)
        ON DELETE CASCADE,
    CONSTRAINT fk_orden_prod_mat_prima_orden
        FOREIGN KEY (amonet_orden_produccion_id)
        REFERENCES amonet_orden_produccion(id_amonet_orden_produccion)
        ON DELETE CASCADE,
    CONSTRAINT uq_orden_prod_materia_prima
        UNIQUE (amonet_materia_prima_id, amonet_orden_produccion_id)
);
