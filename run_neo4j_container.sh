docker run \
    --name neo4j\
    --rm \
    -ti \
    -v $(pwd):/src \
    -v $(pwd)/neodata:/data \
    -p 7474:7474 \
    -p 7687:7687 \
    --env NEO4J_AUTH=neo4j/test \
    --network=ipublica \
    neo4j $1
