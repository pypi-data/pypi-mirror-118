from pycastiphone_client.client import Client


class Cliente:
    _name = "cliente"
    _url_path = "/Cliente"

    def __init__(
        self,
        razonSocial,
        codigo=None,
        nombre=None,
        direccion=None,
        poblacion=None,
        provincia=None,
        cPostal=None,
        telefono=None,
        movil=None,
        fax=None,
        correo=None,
        banco=None,
        cuentaBanco=None,
        bic=None,
        mandatoSepa=None,
        tipoRemesa=None,
        fechaMandato=None,
        primerMandato=None,
        idVendedor=None,
        vencimiento=None,
        iva=None,
        cuentaContable=None,
        comentarios=None,
        tipoCliente=None,
        formaPago=None,
        idioma=None,
        observaciones=None,
        fechaAlta=None,
        facturar=None,
        productos=None,
        telefonos=None,
        **kwargs
    ):
        self.razonSocial = razonSocial
        self.codigo = codigo
        self.nombre = nombre
        self.direccion = direccion
        self.poblacion = poblacion
        self.provincia = provincia
        self.cPostal = cPostal
        self.telefono = telefono
        self.movil = movil
        self.fax = fax
        self.correo = correo
        self.banco = banco
        self.cuentaBanco = cuentaBanco
        self.bic = bic
        self.mandatoSepa = mandatoSepa
        self.tipoRemesa = tipoRemesa
        self.fechaMandato = fechaMandato
        self.primerMandato = primerMandato
        self.idVendedor = idVendedor
        self.vencimiento = vencimiento
        self.iva = iva
        self.cuentaContable = cuentaContable
        self.comentarios = comentarios
        self.tipoCliente = tipoCliente
        self.formaPago = formaPago
        self.idioma = idioma
        self.observaciones = observaciones
        self.fechaAlta = fechaAlta
        self.facturar = facturar
        self.productos = productos 
        self.telefonos = telefonos

    @classmethod
    def create(cls, token, **kwargs):
        """
        Creates a Cliente instance.

        :param kwargs:
        :return:
        """
        response_data = Client(token).put("{}".format(cls._url_path), kwargs)

        return cls(**response_data)
