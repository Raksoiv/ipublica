from neo4j import GraphDatabase
from api import settings


class Neo4jRepository:
    '''
    Neo4j data source
    '''
    def __init__(self):
        self._driver = GraphDatabase.driver(
            settings.NEO4J_URL,
            auth=settings.NEO4J_AUTH,
            encrypted=False,
        )

    def top5_organizations_by_amount(self):
        with self._driver.session() as session:
            result = session.run(
                'MATCH (o:Organismo)<-[:PERTENECE_A]-(:Unidad)'
                '<-[:PERTENECE_A]-(:Licitacion)<-[:ADJUDICO]-(:Proveedor)'
                '-[r:VENDIO]->(i:Item) '
                'WITH o, '
                'SUM(TOINTEGER(r.montoUnitario)) AS montoVentas '
                'RETURN o '
                'ORDER BY montoVentas DESC '
                'LIMIT 5')

            result_list = []

            for record in result:
                record_dict = {}
                for key, value in record[0].items():
                    record_dict[key] = value
                result_list.append(record_dict)

        return result_list

    def top5_providers_by_amount(self):
        with self._driver.session() as session:
            result = session.run(
                'MATCH (p:Proveedor)-[r:VENDIO]->(:Item) '
                'WITH SUM(TOINTEGER(r.montoUnitario)) AS sumMontoUnitario, p '
                'RETURN p '
                'ORDER BY sumMontoUnitario DESC '
                'LIMIT 5'
            )

            result_list = []

            for record in result:
                record_dict = {}
                for key, value in record[0].items():
                    record_dict[key] = value
                result_list.append(record_dict)

        return result_list

    def top5_organism_provider_relations(self):
        with self._driver.session() as session:
            result = session.run(
                'MATCH (o:Organismo)<-[]-(:Unidad)<-[]-(l:Licitacion)'
                '<-[:ADJUDICO]-(p:Proveedor)-[r:VENDIO]->(:Item) '
                'RETURN o, COUNT(l), SUM(TOINTEGER(r.montoUnitario)) '
                'AS sumMontoUnitario, p '
                'ORDER BY sumMontoUnitario DESC '
                'LIMIT 5'
            )

            result_list = []
            for record in result:
                result_dict = {}
                # Organismo
                result_dict['Organismo'] = {}
                for k, v in record[0].items():
                    result_dict['Organismo'][k] = v
                # Cantidad de licitaciones
                result_dict['Licitaciones'] = record[1]
                # Suma montos unitarios
                result_dict['MontosUnitarios'] = record[2]
                # Proveedor
                result_dict['Proveedor'] = {}
                for k, v in record[3].items():
                    result_dict['Proveedor'][k] = v
                result_list.append(result_dict)

            return result_list
