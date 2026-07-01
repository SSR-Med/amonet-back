CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE amonet_tag_kanban (
    id_amonet_tag_kanban UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,
    color_red INT NOT NULL,
    color_green INT NOT NULL,
    color_blue INT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_tag_kanban_nombre UNIQUE (nombre),
    CONSTRAINT uq_tag_kanban_color UNIQUE (color_red, color_green, color_blue),
    CONSTRAINT ck_tag_kanban_color_red CHECK (color_red >= 0 AND color_red <= 255),
    CONSTRAINT ck_tag_kanban_color_green CHECK (color_green >= 0 AND color_green <= 255),
    CONSTRAINT ck_tag_kanban_color_blue CHECK (color_blue >= 0 AND color_blue <= 255)
);
