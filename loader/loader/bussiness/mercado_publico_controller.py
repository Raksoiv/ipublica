import time

from loader.bussiness.input_data_interface import InputDataInterface
from loader.bussiness.output_data_interface import OutputDataInterface
from loader.bussiness.database_interface import DatabaseInterface


class MercadoPublicoController:
    def __init__(
        self,
        input: InputDataInterface,
        neo4j: OutputDataInterface,
        elastic: OutputDataInterface,
        database: DatabaseInterface,
    ):
        self.input = input
        self.neo4j = neo4j
        self.elastic = elastic
        self.database = database

    def get_neo4j_nodes(self, data_dict: dict) -> list:
        nodes = []

        # Add Licitacion node
        nodes.append({
            'id': data_dict['codigoExterno'],
            'label': 'Licitacion',
            'nombre': data_dict['nombre'],
            'descripcion': data_dict['descripcion'],
            'estado': data_dict['estado'],
            'fechaCreacion': data_dict['fechaCreacion'],
            'fechaCierre': data_dict['fechaCierre'],
            'fechaPublicacion': data_dict['fechaPublicacion'],
            'fechaAdjudicacion': data_dict['fechaAdjudicacion'],
            'fecha': data_dict['fecha'],
            'numero': data_dict['numero'],
            'numeroOferentes': data_dict['numeroOferentes'],
            'urlActa': data_dict['urlActa'],
        })

        # Add Persona node
        nodes.append({
            'id': data_dict['emailResponsablePago'],
            'label': 'Persona',
            'nombreResponsablePago': data_dict['nombreResponsablePago'],
        })

        # Add Persona node
        nodes.append({
            'id': data_dict['emailResponsableContrato'],
            'label': 'Persona',
            'nombreResponsableContrato':
                data_dict['nombreResponsableContrato'],
            'fonoResponsableContrato': data_dict['fonoResponsableContrato'],
        })

        # Add Organismo node
        nodes.append({
            'id': data_dict['codigoOrganismo'],
            'label': 'Organismo',
            'nombreOrganismo': data_dict['nombreOrganismo'],
        })

        # Add Unidad node
        nodes.append({
            'id': data_dict['codigoUnidad'],
            'label': 'Unidad',
            'rutUnidad': data_dict['rutUnidad'],
            'nombreUnidad': data_dict['nombreUnidad'],
            'comunaUnidad': data_dict['comunaUnidad'],
            'regionUnidad': data_dict['regionUnidad'],
        })

        # Add Usuario node
        nodes.append({
            'id': data_dict['codigoUsuario'],
            'label': 'Usuario',
            'rutUsuario': data_dict['rutUsuario'],
            'nombreUsuario': data_dict['nombreUsuario'],
            'cargoUsuario': data_dict['cargoUsuario'],
        })

        # Add nodes for the item key
        for item in data_dict['items']:
            # Add Item node
            nodes.append({
                'id': item['codigoProducto'],
                'label': 'Item',
                'codigoCategoria': item['codigoCategoria'],
                'categoria': item['categoria'],
                'nombreProducto': item['nombreProducto'],
                'descripcion': item['descripcion'],
            })

            # Add Proveedor node
            if 'rutProveedor' in item.keys():
                nodes.append({
                    'id': item['rutProveedor'],
                    'label': 'Proveedor',
                    'nombreProveedor': item['nombreProveedor'],
                })

        return nodes

    def get_neo4j_relations(self, data_dict: dict) -> list:
        relations = []

        relations.append({
            'start_id': data_dict['emailResponsablePago'],
            'start_label': 'Persona',
            'relation': 'RESPONSABLE_PAGO',
            'end_id': data_dict['codigoExterno'],
            'end_label': 'Licitacion',
        })

        relations.append({
            'start_id': data_dict['emailResponsableContrato'],
            'start_label': 'Persona',
            'relation': 'RESPONSABLE_CONTRATO',
            'end_id': data_dict['codigoExterno'],
            'end_label': 'Licitacion',
        })

        relations.append({
            'start_id': data_dict['codigoUnidad'],
            'start_label': 'Unidad',
            'relation': 'PERTENECE_A',
            'end_id': data_dict['codigoOrganismo'],
            'end_label': 'Organismo',
        })

        relations.append({
            'start_id': data_dict['codigoExterno'],
            'start_label': 'Licitacion',
            'relation': 'PERTENECE_A',
            'end_id': data_dict['codigoUnidad'],
            'end_label': 'Unidad',
        })

        relations.append({
            'start_id': data_dict['codigoUsuario'],
            'start_label': 'Usuario',
            'relation': 'PERTENECE_A',
            'end_id': data_dict['codigoUnidad'],
            'end_label': 'Unidad',
        })

        relations.append({
            'start_id': data_dict['codigoUsuario'],
            'start_label': 'Usuario',
            'relation': 'CREO',
            'end_id': data_dict['codigoExterno'],
            'end_label': 'Licitacion',
        })

        for item in data_dict['items']:
            if 'rutProveedor' in item.keys():
                relations.append({
                    'start_id': item['rutProveedor'],
                    'start_label': 'Proveedor',
                    'relation': 'ADJUDICO',
                    'end_id': data_dict['codigoExterno'],
                    'end_label': 'Licitacion',
                })
                relations.append({
                    'start_id': item['rutProveedor'],
                    'start_label': 'Proveedor',
                    'relation': 'VENDIO',
                    'end_id': item['codigoProducto'],
                    'end_label': 'Item',
                    'unidadMedida': item['unidadMedida'],
                    'cantidad': item['cantidad'],
                    'montoUnitario': item['montoUnitario'],
                })
            relations.append({
                'start_id': item['codigoProducto'],
                'start_label': 'Item',
                'relation': 'SOLICITADO_POR',
                'end_id': data_dict['codigoExterno'],
                'end_label': 'Licitacion',
            })

        return relations

    def send_neo4j(self, data_id: str):
        if self.database.check_false(data_id, 'neo4j'):
            data_dict = self.input.get_data(data_id)
            neo4j_data = {
                'nodes': self.get_neo4j_nodes(data_dict),
                'relations': self.get_neo4j_relations(data_dict),
            }
            self.neo4j.save(neo4j_data)
            self.database.mark_true(data_id, 'neo4j')

    def send_elastic(self, data_id: str):
        if self.database.check_false(data_id, 'elastic'):
            elastic_doc = self.input.get_data(data_id)
            self.elastic.save(elastic_doc)
            self.database.mark_true(data_id, 'elastic')

    def main(self):
        while True:
            print('loop started')
            for data_id in self.input.list_data_ids():
                self.send_neo4j(data_id)
                self.send_elastic(data_id)
            print('loop ended')
            time.sleep(30 * 60)
