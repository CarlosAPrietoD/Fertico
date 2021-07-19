from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    pos_verify = fields.Selection([('verified','Verificado'),('unverified','Sin verificar')], string="Verificado", default='unverified')

    def action_pos_session_verified(self):        
        self.pos_verify = 'verified'