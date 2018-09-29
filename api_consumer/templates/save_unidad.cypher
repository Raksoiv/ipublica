MATCH (o:Organismo) WHERE o.codigo = $cod_org
MERGE (u:Unidad {codigo:$codigo})
ON CREATE SET u.rut = $rut, u.nombre = $nombre, u.direccion = $direccion, u.comuna = $comuna, u.region = $region
MERGE (o)<-[:Pertenece]-(u)

