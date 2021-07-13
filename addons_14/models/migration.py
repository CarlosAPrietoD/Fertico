from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_gid = fields.Integer()
    additional_info = fields.Char()

    def autocomplete(self):
        return True

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pricelist_id_domain = fields.Integer()
    force = fields.Boolean()
    payment_term_id_domain = fields.Integer()

class StockLocation(models.Model):
    _inherit = 'stock.location'

    allow_negative_stock = fields.Boolean()

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    display_sales = fields.Boolean()