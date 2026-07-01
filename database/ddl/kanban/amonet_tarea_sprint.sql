CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_tarea_sprint (
    id_amonet_tarea_sprint UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    asignado UUID NOT NULL,
    fecha_vencimiento TIMESTAMPTZ NULL,
    tags JSONB NULL,
    amonet_prioridad_kanban_id UUID NULL,
    amonet_sprint_id UUID NOT NULL,
    amonet_columna_kanban_id UUID NOT NULL,
    usuario_alta UUID NOT NULL,
    fecha_alta TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    usuario_modifica UUID NULL,
    fecha_modifica TIMESTAMPTZ NULL,
    CONSTRAINT fk_tarea_sprint_sprint
        FOREIGN KEY (amonet_sprint_id)
        REFERENCES amonet_sprint(id_amonet_sprint)
        ON DELETE CASCADE,
    CONSTRAINT fk_tarea_sprint_columna
        FOREIGN KEY (amonet_columna_kanban_id)
        REFERENCES amonet_columna_kanban(id_amonet_columna_kanban)
        ON DELETE CASCADE,
);
