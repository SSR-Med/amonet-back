CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_inventario_materia_prima (
    id_amonet_inventario_materia_prima UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fecha_ingreso TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    numero_ingreso VARCHAR(50) NOT NULL,
    amonet_materia_prima_id UUID NOT NULL,
    proveedor VARCHAR(255) NOT NULL,
    lote VARCHAR(255) NOT NULL,
    fecha_vencimiento TIMESTAMPTZ NOT NULL,
    usuario_alta UUID NOT NULL,
    status BOOLEAN,
    usuario_modifica UUID,
    fecha_modifica TIMESTAMPTZ,
    ruta_evidencia TEXT NOT NULL,
    observacion_rechazo TEXT,
    CONSTRAINT fk_inventario_materia_prima
        FOREIGN KEY (amonet_materia_prima_id)
        REFERENCES amonet_materia_prima(id_amonet_materia_prima)
        ON DELETE CASCADE
);
