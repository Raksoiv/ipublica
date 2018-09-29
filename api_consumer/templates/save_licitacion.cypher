MERGE (l:Licitacion {codigo:$codigo})
ON CREATE SET l.nombre = $nombre, l.descripcion = $descripcion, l.estado = $estado, l.monto_estimado = $monto_estimado, l.fecha_creacion = $fecha_creacion, l.fecha_cierre = $fecha_cierre, l.fecha_inicio = $fecha_inicio, l.fecha_final = $fecha_final
