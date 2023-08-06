from decimal import Decimal

from nv.utils.collections.structures.serializer import SerializerMixin, SerializerRootlessMixin, SerializerList, \
    SerializerDateTime


__ALL__ = ["InvoiceAddress", "InvoiceIssuer", "InvoiceRecipient",
           "InvoiceProductTax", "InvoiceProductOrder", "InvoiceProduct",
           "InvoiceItemTax", "InvoiceItem",
           "InvoiceFreightCompany", "InvoiceFreightDetail", "InvoiceFreight",
           "InvoicePaymentInvoice", "InvoicePaymentItem", "InvoicePayment",
           "InvoiceHeader", "InvoiceAdditionalInfo", "Invoice",
           "InvoicePackage", "InvoiceSecurityInfo", "InvoiceSecurity", "InvoiceWrapper"
           ]


class InvoiceAddress(SerializerMixin):
    _fields = {
        'street': 'xLgr',
        'number': 'nro',
        'suite': 'xCPl',
        'neighborhood': 'xBairro',
        'municipality_id': 'cMun',
        'municipality': 'xMun',
        'state': 'UF',
        'zip_code': 'CEP',
        'country_id': 'cPais',
        'country': 'xPais',
        'phone': 'fone',
    }


class InvoiceIssuer(SerializerMixin):
    _fields = {
        'tax_id': 'CNPJ',
        'name': 'xNome',
        'address': ('enderEmit', InvoiceAddress),
        'state_tax_id': 'IE',
        'tax_regime_id': 'CRT',
    }


class InvoiceRecipient(SerializerMixin):
    _fields = {
        'tax_id': 'CNPJ',
        'name': 'xNome',
        'address': ('enderDest', InvoiceAddress),
        'state_tax_id': 'IE',
        'tax_regime_id': 'CRT',
        'email': 'email',
        '_indIEDest': 'indIEDest',
    }


class InvoiceProductTax(SerializerRootlessMixin):
    _fields = {
        '_NCM': 'NCM',
        '_CFOP': 'CFOP',
        'tax_EAN': 'cEANTrib',
        'tax_un': 'uTrib',
        'tax_quantity': ('qTrib', Decimal),
        'tax_price': ('vUnTrib', Decimal),
    }


class InvoiceProductOrder(SerializerRootlessMixin):
    _fields = {
        'id': 'xPed',
        'item_id': 'nItemPed'
    }


class InvoiceProduct(SerializerMixin):
    _fields = {
        'id': 'cProd',
        'EAN': 'cEAN',
        'description': 'xProd',
        'un': 'uCom',
        'quantity': ('qCom', Decimal),
        'price': ('vUnCom', Decimal),
        'total': 'vProd',
        'freight_value': ('vFrete', Decimal),
        '_indTot': 'indTot',
        'tax': InvoiceProductTax,
        'order': InvoiceProductOrder,
    }


class InvoiceItemTax(SerializerMixin):
    _fields = {
        '_ICMS': ('ICMS', dict),
        '_IPI': ('IPI', dict),
        '_PIS': ('PIS', dict),
        '_COFINS': ('COFINS', dict),
    }


class InvoiceItem(SerializerMixin):
    _fields = {
        'id': ('@nItem', int),
        'product': ('prod', InvoiceProduct),
        'tax_info': ('imposto', InvoiceItemTax),
    }


class InvoiceFreightCompany(SerializerMixin):
    _fields = {
        'tax_id': 'CNPJ',
        'name': 'xNome',
        'address': 'xEnder',
        'state_tax_id': 'IE',
        'municipality': 'xMun',
        'state': 'UF',
    }


class InvoiceFreightDetail(SerializerMixin):
    _fields = {
        'volumes': 'qVol',
        'spec': 'esp',
        'brand': 'marca',
        'net_weight': 'pesoL',
        'gross_weight': 'pesoB',
    }


class InvoiceFreight(SerializerMixin):
    _fields = {
        'type': 'modFrete',
        'company': ('transporta', InvoiceFreightCompany),
        'details': ('vol', InvoiceFreightDetail),
    }


class InvoicePaymentInvoice(SerializerMixin):
    _fields = {
        'invoices': SerializerList('modFrete'),
        'payments': SerializerList('modFrete'),
    }


class InvoicePaymentItem(SerializerMixin):
    _fields = {
        'id': 'nDup',
        'due_date': SerializerDateTime('dVenc'),
        'amount': ('vDup', Decimal),
    }


class InvoicePayment(SerializerMixin):
    _fields = {
        'invoices': ('fat', InvoicePaymentInvoice),
        'payments': SerializerList('dup', InvoicePaymentItem),
    }


class InvoiceHeader(SerializerMixin):
    _fields = {
        '_cUF': 'cUF',
        '_cNF': 'cNF',
        '_natOp': 'natOp',
        '_indPag': 'indPag',
        '_mod': 'mod',
        'series': 'serie',
        'serial_number': 'nNF',
        'issue_date': SerializerDateTime('dhEmi'),
        'shipping_date': SerializerDateTime('dhSaiEnt'),
        '_tpNF': 'tpNF',
        '_idDest': 'idDest',
        '_cMunFG': 'cMunFG',
        '_tpImp': 'tpImp',
        '_tpEmis': 'tpEmis',
        '_cDV': 'cDV',
        '_tpAmb': 'tpAmb',
        '_finNFe': 'finNFe',
        '_indFinal': 'indFinal',
        '_indPres': 'indPres',
        '_procEmi': 'procEmi',
        '_verProc': 'verProc'
    }


class InvoiceAdditionalInfo(SerializerMixin):
    _fields = {
        'remarks': 'infAdFisco'
    }


class Invoice(SerializerMixin):
    _fields = {
        'header': ('ide', InvoiceHeader),
        'issuer': ('emit', InvoiceIssuer),
        'recipient': ('dest', InvoiceRecipient),
        'items': SerializerList('det', InvoiceItem),
        'total': ('total', dict),
        'freight': ('transp', InvoiceFreight),
        'invoicing': ('cobr', InvoicePayment),
        'additional_info': ('infAdic', InvoiceAdditionalInfo)
    }


class InvoicePackage(SerializerMixin):
    _fields = {
        'invoice': ('infNFe', Invoice),
        'signature': ('Signature', dict)
    }


class InvoiceSecurityInfo(SerializerMixin):
    _fields = {
        '_tpAmb': 'tpAmb',
        '_verAplic': 'verAplic',
        'unique_id': 'chNFe',
        'published_date': SerializerDateTime('dhRecbto'),
        '_nProt': 'nProt',
        '_digVal': 'digVal',
        '_cStat': 'cStat',
        '_xMotivo': 'xMotivo'
    }


class InvoiceSecurity(SerializerMixin):
    _fields = {
        'info': ('infProt', InvoiceSecurityInfo)
    }


class InvoiceWrapper(SerializerMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.content = None

    _root_name = 'nfeProc'
    _fields = {
        'content': ('NFe', InvoicePackage),
        'security': ('protNFe', InvoiceSecurity)
    }
