from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_gid = fields.Integer()