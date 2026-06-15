CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_inventario_materia_prima_contenedor (
    id_amonet_inventario_materia_prima_contenedor UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contador_materia_prima INT NOT NULL,
    cantidad NUMERIC(18,2) NOT NULL,
    precio INT NOT NULL DEFAULT 0,
    amonet_inventario_materia_prima_id UUID NOT NULL,
    CONSTRAINT fk_inventario_contenedor
        FOREIGN KEY (amonet_inventario_materia_prima_id)
        REFERENCES amonet_inventario_materia_prima(id_amonet_inventario_materia_prima)
        ON DELETE CASCADE
);
