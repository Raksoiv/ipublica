import settings
import os.path


class Model:
    @classmethod
    def get_rel_attr(cls):
        return [
            getattr(cls, attr)
            for attr in dir(cls)
            if type(getattr(cls, attr)) == Relation
        ]

    @classmethod
    def init_file(cls):
        # Base File
        filename = cls.__name__.lower()
        filepath = os.path.join(settings.BASE_ETL_PATH, f'{filename}.tsv')
        open(filepath, 'w').close()
        filepath = os.path.join(
            settings.BASE_ETL_PATH, f'{filename}_header.tsv')
        with open(filepath, 'w') as header_file:
            fieldnames = [
                f'{field}:ID({cls.__name__.lower()})'
                if cls.pk == field else field
                for field in cls.fieldnames()
            ]
            header_file.write('\t'.join(fieldnames))
            header_file.write('\t:LABEL')
        # Relations Files
        for rel in cls.get_rel_attr():
            filename = f'{cls.__name__.lower()}_{rel.model.__name__.lower()}'
            filepath = os.path.join(settings.BASE_ETL_PATH, f'{filename}.tsv')
            open(filepath, 'w').close()
            filepath = os.path.join(
                settings.BASE_ETL_PATH, f'{filename}_header.tsv')
            with open(filepath, 'w') as header_file:
                fieldnames = [
                    f':START_ID({cls.__name__.lower()})',
                    *rel.extra_fields,
                    f':END_ID({rel.model.__name__.lower()})',
                    ':TYPE',
                ]
                header_file.write('\t'.join(fieldnames))

    def save(self, model_buf):
        filename = self.__class__.__name__.lower()
        filepath = os.path.join(settings.BASE_ETL_PATH, f'{filename}.tsv')
        with open(filepath, 'a') as data_file:
            if str(getattr(self, self.pk)) not in model_buf:
                data = [
                    str(getattr(self, field)).replace(
                        '"', '').replace('\'', '')
                    for field in self.fieldnames()
                ]
                text_data = '\t'.join(data)
                data_file.write(f'{text_data}\t{self.__class__.__name__}\n')
                model_buf.append(str(getattr(self, self.pk)))

    def save_relation(self, rel_obj, rel_buf, data=[]):
        rel_classes = [rel.model for rel in self.get_rel_attr()]
        assert type(rel_obj) in rel_classes, (
            f'Object {type(rel_obj)} is not a relation'
            f' in the {type(self)} object')
        rel_class = self.get_rel_attr()[rel_classes.index(type(rel_obj))]
        filename = (
            f'{self.__class__.__name__.lower()}'
            f'_{rel_obj.__class__.__name__.lower()}')
        filepath = os.path.join(settings.BASE_ETL_PATH, f'{filename}.tsv')
        self_pk = getattr(self, self.pk)
        rel_pk = getattr(rel_obj, rel_obj.pk)
        with open(filepath, 'a') as data_file:
            if (self_pk, rel_pk) not in rel_buf:
                data = [self_pk, *data, rel_pk, rel_class.rel_type]
                text_data = '\t'.join([str(d) for d in data])
                data_file.write(f'{text_data}\n')
                rel_buf.append((self_pk, rel_pk))


class Relation:
    def __init__(self, model, rel_type, extra_fields=[]):
        self.model = model
        self.rel_type = rel_type.upper()
        self.extra_fields = [*extra_fields, ]


class Product(Model):
    pk = 'codigo'

    def __init__(self, data):
        self.codigo = data['CodigoProducto']
        self.codigo_categoria = data['CodigoCategoria']
        self.categoria = data['Categoria']
        self.nombre = data['NombreProducto']
        self.descripcion = data['Descripcion']
        self.unidad_medida = data['UnidadMedida']
        self.cantidad = data['Cantidad']

    def __str__(self):
        return f'Producto ({self.codigo}) {self.nombre}'

    @staticmethod
    def fieldnames():
        return [
            'codigo',
            'codigo_categoria',
            'categoria',
            'nombre',
            'descripcion',
            'unidad_medida',
            'cantidad',
        ]


class Bidding(Model):
    pk = 'codigo_externo'

    product = Relation(Product, 'needs')

    def __init__(self, data):
        self.codigo_externo = data['CodigoExterno']
        self.nombre = data['Nombre']
        self.codigo_estado = data['CodigoEstado']
        self.descripcion = data['Descripcion']

    def __str__(self):
        return f'Licitación ({self.codigo_externo}) {self.nombre}'

    @staticmethod
    def fieldnames():
        return [
            'codigo_externo',
            'nombre',
            'codigo_estado',
            'descripcion',
        ]


class Organism(Model):
    pk = 'codigo'

    def __init__(self, data):
        data = data['Comprador']
        self.codigo = data['CodigoOrganismo']
        self.nombre = data['NombreOrganismo']

    def __str__(self):
        return f'Organismo ({self.codigo}) {self.nombre}'

    @staticmethod
    def fieldnames():
        return [
            'codigo',
            'nombre',
        ]


class Unit(Model):
    pk = 'rut'

    organism = Relation(Organism, 'belongs_to')

    def __init__(self, data):
        data = data['Comprador']
        self.rut = data['RutUnidad']
        self.codigo = data['CodigoUnidad']
        self.nombre = data['NombreUnidad']
        self.direccion = data['DireccionUnidad']
        self.comuna = data['ComunaUnidad']
        self.region = data['RegionUnidad']

    def __str__(self):
        return f'Unidad ({self.codigo}) {self.nombre}'

    @staticmethod
    def fieldnames():
        return [
            'rut',
            'codigo',
            'nombre',
            'direccion',
            'comuna',
            'region',
        ]


class User(Model):
    # PK
    pk = 'codigo'

    # Relations
    bidding = Relation(Bidding, 'created')
    unit = Relation(Unit, 'works_in')

    def __init__(self, data):
        data = data['Comprador']
        self.rut = data['RutUsuario']
        self.codigo = data['CodigoUsuario']
        self.nombre = data['NombreUsuario']
        self.cargo = data['CargoUsuario']

    def __str__(self):
        return f'Usuario ({self.rut}) {self.nombre}'

    @staticmethod
    def fieldnames():
        return [
            'codigo',
            'rut',
            'nombre',
            'cargo',
        ]


class Provider(Model):
    pk = 'rut'

    bidding = Relation(
        Bidding,
        'awarded',
        ['codigo', 'cantidad', 'monto_unitario'])

    def __init__(self, data):
        self.rut = data['RutProveedor']
        self.nombre = data['NombreProveedor']
        self.cantidad = data['Cantidad']
        self.monto_unitario = data['MontoUnitario']

    def __str__(self):
        return f'Proveedor ({self.rut}) {self.nombre}'

    @staticmethod
    def fieldnames():
        return [
            'rut',
            'nombre',
            'cantidad',
            'monto_unitario',
        ]
