docker run --name elastic --network=ipublica -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.0.1
