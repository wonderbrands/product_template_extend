from odoo import models, fields, api, _
import logging

logging.basicConfig(filename='product_template_extend.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Sub products
    sub_product_line_ids = fields.One2many(related='bom_ids.bom_line_ids', string='Componentes', readonly=True)
    is_kit = fields.Boolean(string='Es un kit?',
                            help='Este campo estará marcado si el SKU es combo o tiene lista de materiales',
                            compute='_is_kit')
    component_list = fields.Boolean(string='Lista de componentes',
                                    help='Este campo estará marcado si el SKU es combo o tiene lista de materiales',
                                    compute='_id_bill_list')
    combo_qty = fields.Float(string='Total combos',
                             help='Muestra la cantidad de combos que se pueden realizar con la lista de materiales actual',
                             compute='_total_combos')

    # Stock
    stock_real = fields.Integer(string="Stock Real", help='muestra el stock real')

    # Calculated measures
    is_calculated_combo = fields.Boolean(string='Es combo', compute='calculated_measures')
    calculated_weight = fields.Float(string='Peso calculado',
                                     help='Muestra el cálculo del peso de los componentes del combo en kilogramos')
    calculated_volume = fields.Float(string='Volumen calculado',
                                     help='Muestra el cálculo del volumen de los componentes del combo, transforma centimetros cúbicos a Litros')


    # Function that evaluates if product is combo or kit
    @api.depends('bom_count')
    def _is_kit(self):
        self.ensure_one()
        #_logger = logging.getLogger(__name__)
        if self.bom_count > 0:
            self.is_kit = True
        else:
            self.is_kit = False

    @api.depends('bill_list')
    def _total_combos(self):
        _logger.info("\n\n")
        _logger.info(self.bill_list.id)
        if self.bom_count > 0 and self.bill_list:
            bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', self.bill_list.id)])
            _logger.info(bom_line_ids)
            _logger.info("\n\n")
            for each in bom_line_ids:
                combo_calculation = each.combo_qty
                self.combo_qty = combo_calculation
        else:
            self.combo_qty = 0.0


    def _id_bill_list(self):
        bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', self.bill_list.id)])
        self.component_list = True
        self.sub_product_line_ids = bom_line_ids


    # Calcula el peso y volumen para combos
    #@api.depends('length', 'width', 'height', 'weight')
    def calculated_measures(self):
        if self.bom_count > 0:
            weight_measures = []
            length_measures = []
            height_measures = []
            width_measures = []
            volume_calculation = []

            # Obtener las líneas de la lista de materiales (BOM)
            bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', self.bill_list.id)])
            product_ids = bom_line_ids.mapped('product_id')

            for product in product_ids:
                # Peso
                weight = product.packing_weight
                weight_measures.append(weight)
                # Largo
                length = product.packing_length
                length_measures.append(length)
                # Alto
                height = product.packing_height
                height_measures.append(height)
                # Ancho
                width = product.packing_width
                width_measures.append(width)

            # Verificar que las listas no estén vacías antes de usar max() y sum()
            if length_measures:
                max_length = max(length_measures)
            else:
                max_length = 0

            if height_measures:
                max_height = max(height_measures)
            else:
                max_height = 0

            if width_measures:
                sum_width = sum(width_measures)
            else:
                sum_width = 0

            self.calculated_volume = (max_length * max_height * sum_width) / 1000
            self.calculated_weight = sum(weight_measures) if weight_measures else 0
            self.is_calculated_combo = True
        else:
            self.is_calculated_combo = False
