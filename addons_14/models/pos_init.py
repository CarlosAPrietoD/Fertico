from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    pos_verify = fields.Boolean(string="Verificado")

    def action_pos_session_verified(self):        
        self.pos_verify = True
