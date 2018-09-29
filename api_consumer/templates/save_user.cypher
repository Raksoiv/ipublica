MATCH (u:Unidad) WHERE u.codigo = $cod_unidad
MATCH (l:Licitacion) WHERE l.codigo = $cod_licitacion
MERGE (user:Usuario {codigo:$codigo})
ON CREATE SET user.rut = $rut, user.nombre = $nombre, user.cargo = $cargo
MERGE (u)<-[:Trabaja]-(user)
MERGE (user)-[:Creador]->(l)
