from odoo import models, fields, api
from datetime import datetime

class ProductProduct(models.Model):
    _inherit = 'product.product'

    estimated_sale=fields.Float(string='Estimated Sale Price', compute='_compute_sale')

    @api.multi
    @api.depends('qty_at_date')
    def _compute_sale(self):
        #calculate the estimated sale price for valuation
        for prod in self:
            prod.estimated_sale=prod.list_price*prod.qty_at_date



class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'


    def open_table_manager(self):

        if self.compute_at_date:
            tree_view_id = self.env.ref('fertico-addons.view_stock_manager_tree').id
            form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.
            action = {
                'type': 'ir.actions.act_window',
                'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                'view_mode': 'tree,form',
                'name': 'Products',
                'res_model': 'product.product',
                'domain': "[('type', '=', 'product'), ('qty_available', '!=', 0)]",
                'context': dict(self.env.context, to_date=self.date, company_owned=True),
            }
            return action
        else:
            tree_view_id = self.env.ref('fertico-addons.view_stock_manager_tree').id
            form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
            # We dont pass `to_date` in the context so that `qty_available` will be computed across
            action = {
                'type': 'ir.actions.act_window',
                'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                'view_mode': 'tree,form',
                'name': 'Products',
                'res_model': 'product.product',
                'domain': "[('type', '=', 'product'), ('qty_available', '!=', 0)]",
                'context': dict(self.env.context, to_date=datetime.now(), company_owned=True),
            }
            return action