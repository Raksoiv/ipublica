#!/usr/bin/env sh

base_folder=$1

neo4j-admin import --delimiter "\t" \
    --nodes "data/etl/bidding_header.tsv,data/etl/bidding.tsv" \
    --nodes "data/etl/organism_header.tsv,data/etl/organism.tsv" \
    --nodes "data/etl/product_header.tsv,data/etl/product.tsv" \
    --nodes "data/etl/provider_header.tsv,data/etl/provider.tsv" \
    --nodes "data/etl/unit_header.tsv,data/etl/unit.tsv" \
    --nodes "data/etl/user_header.tsv,data/etl/user.tsv" \
    --relationships "data/etl/bidding_product_header.tsv,data/etl/bidding_product.tsv" \
    --relationships "data/etl/provider_bidding_header.tsv,data/etl/provider_bidding.tsv" \
    --relationships "data/etl/unit_organism_header.tsv,data/etl/unit_organism.tsv" \
    --relationships "data/etl/user_bidding_header.tsv,data/etl/user_bidding.tsv" \
    --relationships "data/etl/user_unit_header.tsv,data/etl/user_unit.tsv"
