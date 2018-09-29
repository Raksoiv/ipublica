import os.path
from neo4j_orm import Neo4jConnector

TEMPLATES_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates')


class Licitacion:
    def __init__(self, data):
        self.codigo = data['CodigoExterno']
        self.nombre = data['Nombre']
        self.descripcion = data['Descripcion']
        self.estado = data['Estado']
        self.monto_estimado = data['MontoEstimado']

        # Fechas
        fechas = data['Fechas']
        self.fecha_creacion = fechas['FechaCreacion']
        self.fecha_cierre = fechas['FechaCierre']
        self.fecha_inicio = fechas['FechaInicio']
        self.fecha_final = fechas['FechaFinal']

    def save(self):
        conn = Neo4jConnector()
        t = open(os.path.join(TEMPLATES_FOLDER, 'save_licitacion.cypher'), 'r')
        with conn.driver.session() as session:
            session.run(
                t.read(),
                codigo=self.codigo,
                nombre=self.nombre,
                descripcion=self.descripcion,
                estado=self.estado,
                monto_estimado=self.monto_estimado,
                fecha_creacion=self.fecha_creacion,
                fecha_cierre=self.fecha_cierre,
                fecha_inicio=self.fecha_inicio,
                fecha_final=self.fecha_final)


class Organismo:
    def __init__(self, data):
        self.codigo = data['CodigoOrganismo']
        self.nombre = data['NombreOrganismo']

    def save(self):
        conn = Neo4jConnector()
        t = open(os.path.join(TEMPLATES_FOLDER, 'save_organismo.cypher'), 'r')
        with conn.driver.session() as session:
            session.run(
                t.read(),
                codigo=self.codigo,
                nombre=self.nombre)


class Unidad:
    def __init__(self, data):
        self.codigo = data['CodigoUnidad']
        self.rut = data['RutUnidad']
        self.nombre = data['NombreUnidad']
        self.direccion = data['DireccionUnidad']
        self.comuna = data['ComunaUnidad']
        self.region = data['RegionUnidad']

    def save(self, org):
        conn = Neo4jConnector()
        t = open(os.path.join(TEMPLATES_FOLDER, 'save_unidad.cypher'), 'r')
        with conn.driver.session() as session:
            session.run(
                t.read(),
                cod_org=org.codigo,
                codigo=self.codigo,
                rut=self.rut,
                nombre=self.nombre,
                direccion=self.direccion,
                comuna=self.comuna,
                region=self.region)


class Usuario:
    def __init__(self, data):
        self.codigo = data['CodigoUsuario']
        self.rut = data['RutUsuario']
        self.nombre = data['NombreUsuario']
        self.cargo = data['CargoUsuario']

    def save(self, licitacion, unidad):
        conn = Neo4jConnector()
        t = open(os.path.join(TEMPLATES_FOLDER, 'save_user.cypher'), 'r')
        with conn.driver.session() as session:
            session.run(
                t.read(),
                cod_unidad=unidad.codigo,
                cod_licitacion=licitacion.codigo,
                codigo=self.codigo,
                rut=self.rut,
                nombre=self.nombre,
                cargo=self.cargo)
