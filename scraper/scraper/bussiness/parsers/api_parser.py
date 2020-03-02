import json
import logging

logger = logging.getLogger(__name__)


class APIParser:
    def parse_day(self, json_str: str) -> list:
        json_dict = json.loads(json_str)
        bidding_list = json_dict['Listado']
        bidding_id_list = []
        for bidding in bidding_list:
            bidding_id_list.append(bidding['CodigoExterno'])
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
                'codigoOrganismo': bidding_data['Comprador']['CodigoOrganismo'],
                'nombreOrganismo': bidding_data['Comprador']['NombreOrganismo'],
                'rutUnidad': bidding_data['Comprador']['RutUnidad'],
                'codigoUnidad': bidding_data['Comprador']['CodigoUnidad'],
                'nombreUnidad': bidding_data['Comprador']['NombreUnidad'],
                'comunaUnidad': bidding_data['Comprador']['ComunaUnidad'],
                'regionUnidad': bidding_data['Comprador']['RegionUnidad'],
                'rutUsuario': bidding_data['Comprador']['RutUsuario'],
                'codigoUsuario': bidding_data['Comprador']['CodigoUsuario'],
                'nombreUsuario': bidding_data['Comprador']['NombreUsuario'],
                'cargoUsuario': bidding_data['Comprador']['CargoUsuario'],
                'fechaCreacion': bidding_data['Fechas']['FechaCreacion'],
                'fechaCierre': bidding_data['Fechas']['FechaCierre'],
                'fechaPublicacion': bidding_data['Fechas']['FechaPublicacion'],
                'fechaAdjudicacion': bidding_data['Fechas']['FechaAdjudicacion'],
                'nombreResponsablePago': bidding_data['NombreResponsablePago'],
                'emailResponsablePago': bidding_data['EmailResponsablePago'],
                'nombreResponsableContrato':
                    bidding_data['NombreResponsableContrato'],
                'emailResponsableContrato':
                    bidding_data['EmailResponsableContrato'],
                'fonoResponsableContrato':
                    bidding_data['FonoResponsableContrato'],
                'fecha': bidding_data['Adjudicacion']['Fecha'],
                'numero': bidding_data['Adjudicacion']['Numero'],
                'numeroOferentes':
                    bidding_data['Adjudicacion']['NumeroOferentes'],
                'urlActa': bidding_data['Adjudicacion']['UrlActa'],
                'items': [
                    {
                        'codigoProducto': item['CodigoProducto'],
                        'codigoCategoria': item['CodigoCategoria'],
                        'categoria': item['Categoria'],
                        'nombreProducto': item['NombreProducto'],
                        'descripcion': item['Descripcion'],
                        'unidadMedida': item['UnidadMedida'],
                        'cantidad': item['Cantidad'],
                        'rutProveedor': item['Adjudicacion']['RutProveedor'],
                        'nombreProveedor':
                            item['Adjudicacion']['NombreProveedor'],
                        'cantidad': item['Adjudicacion']['Cantidad'],
                        'montoUnitario': item['Adjudicacion']['MontoUnitario'],
                    } for item in bidding_data['Items']['Listado']
                ]
            }
        except TypeError:
            logger.error('Couldn\'t parse JSON response')
            logging.error(json_str)
            raise

        return bidding_doc
