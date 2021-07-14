from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_gid = fields.Integer()
    additional_info = fields.Char()

    def autocomplete(self):
        return True

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pricelist_id_domain = fields.Integer(required=False)
    force = fields.Boolean()
    payment_term_id_domain = fields.Integer(required=False)

    api.onchange('pricelist_id')
    def change_pricelist(self):
        self.pricelist_id_domain = self.pricelist_id

    api.onchange('payment_term_id')
    def change_term(self):
        self.payment_term_id_domain = self.payment_term_id


class StockLocation(models.Model):
    _inherit = 'stock.location'

    allow_negative_stock = fields.Boolean()

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    display_sales = fields.Boolean()
    force_term = fields.Boolean()
