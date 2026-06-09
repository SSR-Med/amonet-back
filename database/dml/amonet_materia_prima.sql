INSERT INTO amonet_materia_prima (nombre, id_cat_amonet_tipo_materia_prima, id_cat_amonet_tipo_unidad)
VALUES
    ('HARINA DE TRIGO',  (SELECT id_cat_amonet_tipo_materia_prima FROM cat_amonet_tipo_materia_prima WHERE nombre = 'QUIMICO'),     (SELECT id_cat_amonet_tipo_unidad FROM cat_amonet_tipo_unidad WHERE nombre = 'KILOGRAMOS')),
    ('AZÚCAR REFINADA',  (SELECT id_cat_amonet_tipo_materia_prima FROM cat_amonet_tipo_materia_prima WHERE nombre = 'QUIMICO'),     (SELECT id_cat_amonet_tipo_unidad FROM cat_amonet_tipo_unidad WHERE nombre = 'KILOGRAMOS')),
    ('ACEITE VEGETAL',   (SELECT id_cat_amonet_tipo_materia_prima FROM cat_amonet_tipo_materia_prima WHERE nombre = 'QUIMICO'),     (SELECT id_cat_amonet_tipo_unidad FROM cat_amonet_tipo_unidad WHERE nombre = 'LITROS')),
    ('ETIQUETA FRENTE',  (SELECT id_cat_amonet_tipo_materia_prima FROM cat_amonet_tipo_materia_prima WHERE nombre = 'ETIQUETADO'), (SELECT id_cat_amonet_tipo_unidad FROM cat_amonet_tipo_unidad WHERE nombre = 'UNIDADES')),
    ('CAJA DE CARTÓN',   (SELECT id_cat_amonet_tipo_materia_prima FROM cat_amonet_tipo_materia_prima WHERE nombre = 'EMPAQUETADO'),(SELECT id_cat_amonet_tipo_unidad FROM cat_amonet_tipo_unidad WHERE nombre = 'UNIDADES'));
