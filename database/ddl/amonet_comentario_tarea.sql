CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_comentario_tarea (
    id_amonet_comentario_tarea UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    amonet_tarea_sprint_id UUID NOT NULL,
    comentario TEXT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    usuario_alta UUID NOT NULL,
    fecha_alta TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_modifica TIMESTAMPTZ NULL,
    CONSTRAINT fk_comentario_tarea_tarea
        FOREIGN KEY (amonet_tarea_sprint_id)
        REFERENCES amonet_tarea_sprint(id_amonet_tarea_sprint)
        ON DELETE CASCADE
);
