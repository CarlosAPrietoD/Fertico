from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _get_domain_tag(self):
        company=self.env.user.company_id.name
        if company != 'Logistica Capitan, S.A. de C.V.':
            domain=[('name','not ilike',"v:")]
            return domain

    analytic_tag_ids = fields.Many2many('account.analytic.tag', domain=_get_domain_tag)


    