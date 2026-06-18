CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_orden_produccion (
    id_amonet_orden_produccion UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    observacion_creacion TEXT,
    amonet_producto_id UUID NOT NULL,
    fecha_alta TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    usuario_alta UUID NOT NULL,
    fecha_modifica TIMESTAMPTZ,
    usuario_modifica UUID,
    amonet_estado_produccion_id UUID NOT NULL,
    CONSTRAINT fk_orden_produccion_producto
        FOREIGN KEY (amonet_producto_id)
        REFERENCES amonet_producto(id_amonet_producto)
        ON DELETE CASCADE,
    CONSTRAINT fk_orden_produccion_estado
        FOREIGN KEY (amonet_estado_produccion_id)
        REFERENCES cat_amonet_estado_produccion(id_cat_amonet_estado_produccion)
        ON DELETE CASCADE
);
