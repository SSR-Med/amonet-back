CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_orden_produccion_variable_global (
    id_amonet_orden_produccion_variable_global UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    amonet_orden_produccion_id UUID NOT NULL,
    amonet_variable_materia_prima_id UUID NOT NULL,
    cantidad INT NOT NULL,
    CONSTRAINT fk_orden_prod_var_global_orden
        FOREIGN KEY (amonet_orden_produccion_id)
        REFERENCES amonet_orden_produccion(id_amonet_orden_produccion)
        ON DELETE CASCADE,
    CONSTRAINT fk_orden_prod_var_global_variable
        FOREIGN KEY (amonet_variable_materia_prima_id)
        REFERENCES amonet_variable_materia_prima(id_amonet_variable_materia_prima)
        ON DELETE CASCADE,
    CONSTRAINT uq_orden_prod_var_global
        UNIQUE (amonet_orden_produccion_id, amonet_variable_materia_prima_id),
    CONSTRAINT ck_orden_prod_var_global_cantidad CHECK (cantidad > 0)
);
