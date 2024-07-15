import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
from io import StringIO, BytesIO
import logging
import json
import requests

class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Modelo para creación de marcas de producto"

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')
    supplier = fields.Many2one('res.partner', string='Proveedor')

class InternalCategory(models.Model):
    _name = "internal.category"
    _description = "Modelo que incluye un catálogo de categorías internas para el Owner y Comprador"

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    #Number of Packages
    packages_number = fields.Integer(string='Numero de Paquetes')
    #Product Measurements
    product_length = fields.Float(string='Largo producto', help="Largo del Producto en centimentros")
    product_height = fields.Float(string='Alto producto', help="Alto del Producto en centimentros")
    product_width = fields.Float(string='Ancho producto', help="Ancho del Producto en centimentros")
    product_weight = fields.Float(string='Peso producto', help="Peso del Producto en kilogramos")
    product_volume = fields.Float(string='Volumen producto', help="Volumen del Producto", compute='_volumen')
    #Packaging Measurements
    packing_length = fields.Float(string='Largo empaque', help="Largo del Empaque en centimentros")
    packing_height = fields.Float(string='Alto empaque', help="Alto del Empaque en centimentros")
    packing_width = fields.Float(string='Ancho empaque', help="Ancho del Empaque en centimentros")
    packing_weight = fields.Float(string='Peso empaque', help="Peso del Empaque en centimentros")

    # Comercial
    buyer = fields.Many2one('res.partner', string='Comprador responsable',
                            help='Establece el comprador encargado de este SKU')
    owner = fields.Many2one('res.partner', string='Owner comercial',
                            help='Establece el comercial responsable de este SKU')
    internal_category = fields.Many2one('internal.category', string='Categoría interna',
                                        help='Categoría interna para el equipo de SR')
    brand = fields.Many2one('product.brand', string='Marca', help='Marca a la que pertecene el SKU')


    # Product Status
    status = fields.Many2one('product.estatus', string='Estatus', help='Estatus del producto')
    substatus = fields.Many2one('product.subestatus', string='Subestatus',
                                help='Subestatus del producto')  # , domain=[('status_subsequence', "=", 'status_sequence')])
    #status_sequence = fields.Char(related='status.sequence', string='Secuencia')
    #status_subsequence = fields.Char(related='substatus.subsequence', string='Subsecuencia')
    # Seasonal and Period
    start_period = fields.Char(string='Inicio del periodo',
                               help='Fecha/Mes en que inicia una estación o un Periodo para un SKU')
    end_period = fields.Char(string='Fin del periodo',
                             help='Fecha/Mes en que finaliza una estación o un Periodo para un SKU')

    # Lista de materiales
    bill_list = fields.Many2one('mrp.bom', 'Lista de materiales')

    # Function that print the volume of product
    @api.depends('product_width', 'product_height', 'product_length')
    def _volumen(self):
        #_logger = logging.getLogger(__name__)
        for rec in self:
            if rec.product_width > 0 and rec.product_height > 0 and rec.product_length > 0:
                rec.product_volume = round((rec.product_width * rec.product_height * rec.product_length) / 5000, 2)
            else:
                rec.product_volume = 0.00

