MERGE (o:Organismo {codigo:$codigo})
ON CREATE SET o.nombre = $nombre
