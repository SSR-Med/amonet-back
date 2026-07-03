CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_orden_produccion_materia_prima_contenedor (
    id_amonet_orden_produccion_materia_prima_contenedor UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    amonet_inventario_materia_prima_contenedor_id UUID NOT NULL,
    amonet_orden_produccion_materia_prima_id UUID NOT NULL,
    cantidad INT NOT NULL,
    coste NUMERIC(18,2) NOT NULL,
    CONSTRAINT fk_orden_prod_mat_prima_cont_inventario
        FOREIGN KEY (amonet_inventario_materia_prima_contenedor_id)
        REFERENCES amonet_inventario_materia_prima_contenedor(id_amonet_inventario_materia_prima_contenedor)
        ON DELETE CASCADE,
    CONSTRAINT fk_orden_prod_mat_prima_cont_orden
        FOREIGN KEY (amonet_orden_produccion_materia_prima_id)
        REFERENCES amonet_orden_produccion_materia_prima(id_amonet_orden_produccion_materia_prima)
        ON DELETE CASCADE,
    CONSTRAINT uq_orden_prod_mat_prima_cont
        UNIQUE (amonet_inventario_materia_prima_contenedor_id, amonet_orden_produccion_materia_prima_id),
    CONSTRAINT ck_orden_prod_mat_prima_cont_cantidad CHECK (cantidad > 0),
    CONSTRAINT ck_orden_prod_mat_prima_cont_coste CHECK (coste > 0)
);
