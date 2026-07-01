CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_columna_kanban (
    id_amonet_columna_kanban UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,
    posicion INT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    usuario_alta UUID NOT NULL,
    fecha_alta TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    usuario_modifica UUID NULL,
    fecha_modifica TIMESTAMPTZ NULL,
    CONSTRAINT uq_columna_kanban_posicion UNIQUE (posicion),
    CONSTRAINT ck_columna_kanban_posicion CHECK (posicion > 0)
);

CREATE UNIQUE INDEX uq_columna_kanban_nombre_activo ON amonet_columna_kanban(nombre) WHERE activo = TRUE;
