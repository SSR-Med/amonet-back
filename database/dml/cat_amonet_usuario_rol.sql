INSERT INTO cat_amonet_usuario_rol (nombre) VALUES ('ADMIN') ON CONFLICT (nombre) DO NOTHING;
INSERT INTO cat_amonet_usuario_rol (nombre) VALUES ('OPERARIO') ON CONFLICT (nombre) DO NOTHING;
INSERT INTO cat_amonet_usuario_rol (nombre) VALUES ('CALIDAD') ON CONFLICT (nombre) DO NOTHING;
INSERT INTO cat_amonet_usuario_rol (nombre) VALUES ('JEFE_PRODUCCION') ON CONFLICT (nombre) DO NOTHING;
INSERT INTO cat_amonet_usuario_rol (nombre) VALUES ('TODERO') ON CONFLICT (nombre) DO NOTHING;
