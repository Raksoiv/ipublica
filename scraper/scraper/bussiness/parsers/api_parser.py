import json
import logging

logger = logging.getLogger(__name__)


class APIParser:
    def parse_day(self, json_str: str) -> list:
        json_dict = json.loads(json_str)
        try:
            bidding_list = json_dict['Listado']
            bidding_id_list = []
            for bidding in bidding_list:
                bidding_id_list.append(bidding['CodigoExterno'])
        except TypeError:
            return None
        return bidding_id_list

    def parse_bidding(self, json_str: str) -> dict:
        json_dict = json.loads(json_str)
        try:
            bidding_data = json_dict['Listado'][0]
            bidding_doc = {
                'codigoExterno': bidding_data['CodigoExterno'],
                'nombre': bidding_data['Nombre'],
                'descripcion': bidding_data['Descripcion'],
                'estado': bidding_data['Estado'],
                'nombreResponsablePago': bidding_data['NombreResponsablePago'],
                'emailResponsablePago': bidding_data['EmailResponsablePago'],
                'nombreResponsableContrato':
                    bidding_data['NombreResponsableContrato'],
                'emailResponsableContrato':
                    bidding_data['EmailResponsableContrato'],
                'fonoResponsableContrato':
                    bidding_data['FonoResponsableContrato'],
                'codigoOrganismo':
                    bidding_data['Comprador']['CodigoOrganismo'],
                'nombreOrganismo':
                    bidding_data['Comprador']['NombreOrganismo'],
            }
            if bidding_data['Comprador'] is not None:
                bidding_doc.update({
                    'rutUnidad': bidding_data['Comprador']['RutUnidad'],
                    'codigoUnidad': bidding_data['Comprador']['CodigoUnidad'],
                    'nombreUnidad': bidding_data['Comprador']['NombreUnidad'],
                    'comunaUnidad': bidding_data['Comprador']['ComunaUnidad'],
                    'regionUnidad': bidding_data['Comprador']['RegionUnidad'],
                    'rutUsuario': bidding_data['Comprador']['RutUsuario'],
                    'codigoUsuario':
                        bidding_data['Comprador']['CodigoUsuario'],
                    'nombreUsuario':
                        bidding_data['Comprador']['NombreUsuario'],
                    'cargoUsuario':
                        bidding_data['Comprador']['CargoUsuario'],
                })

            if bidding_data['Fechas'] is not None:
                bidding_doc.update({
                    'fechaCreacion': bidding_data['Fechas']['FechaCreacion'],
                    'fechaCierre': bidding_data['Fechas']['FechaCierre'],
                    'fechaPublicacion':
                        bidding_data['Fechas']['FechaPublicacion'],
                    'fechaAdjudicacion':
                        bidding_data['Fechas']['FechaAdjudicacion'],
                })

            if bidding_data['Adjudicacion'] is not None:
                bidding_doc.update({
                    'fecha': bidding_data['Adjudicacion']['Fecha'],
                    'numero': bidding_data['Adjudicacion']['Numero'],
                    'numeroOferentes':
                        bidding_data['Adjudicacion']['NumeroOferentes'],
                    'urlActa': bidding_data['Adjudicacion']['UrlActa'],
                })

            bidding_doc['items'] = []
            for item in bidding_data['Items']['Listado']:
                item_data = {
                    'codigoProducto': item['CodigoProducto'],
                    'codigoCategoria': item['CodigoCategoria'],
                    'categoria': item['Categoria'],
                    'nombreProducto': item['NombreProducto'],
                    'descripcion': item['Descripcion'],
                    'unidadMedida': item['UnidadMedida'],
                    'cantidad': item['Cantidad'],
                }
                if item['Adjudicacion'] is not None:
                    item_data.update({
                        'rutProveedor': item['Adjudicacion']['RutProveedor'],
                        'nombreProveedor':
                            item['Adjudicacion']['NombreProveedor'],
                        'cantidad': item['Adjudicacion']['Cantidad'],
                        'montoUnitario': item['Adjudicacion']['MontoUnitario'],
                    })
                bidding_doc['items'].append(item_data)
        except TypeError:
            logger.error('Couldn\'t parse JSON response')
            logging.error(json_str)
            return None

        return bidding_doc
