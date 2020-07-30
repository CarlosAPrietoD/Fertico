from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, values):
        if values.get('parent_id'):
            if values.get('vat'):
                parent_vat= self.env['res.partner'].search([('id', '=', values.get('parent_id'))])
                if values['vat'] != parent_vat:
                    if values['vat'] != "XAXX010101000":
                        dup_ids = self.env['res.partner'].search([('vat', '=', values['vat'])])
                        if dup_ids:
                            raise Warning('RFC debe ser unico, este ya ha sido registrado!')
        else:
            if values.get('vat'):
                if values['vat']:
                    if values['vat'] != "XAXX010101000":
                        dup_ids = self.env['res.partner'].search([('vat', '=', values['vat'])])
                        if dup_ids:
                            raise Warning('RFC debe ser unico, este ya ha sido registrado!')
            
        contact = super(ResPartner, self).create(values)

        return contact

    @api.multi
    def write(self, values):

        if values.get('parent_id'):
            if values.get('vat'):
                parent_vat= self.env['res.partner'].search([('id', '=', values.get('parent_id'))])
                if values['vat'] != parent_vat:
                    if values['vat'] != "XAXX010101000":
                        dup_ids = self.env['res.partner'].search([('vat', '=', values['vat'])])
                        if dup_ids:
                            raise Warning('RFC debe ser unico, este ya ha sido registrado!')
        else:
            for contact in self:
                if contact.parent_id:
                    if values.get('vat'):
                        parent_vat= contact.env['res.partner'].search([('id', '=', contact.parent_id.id)]).vat
                        if values['vat'] != parent_vat:
                            if values['vat'] != "XAXX010101000":
                                dup_ids = contact.env['res.partner'].search([('vat', '=', values['vat'])])
                                if dup_ids:
                                    raise Warning('RFC debe ser unico, este ya ha sido registrado!')
                else:
                    if values.get('vat'):
                        if values['vat']:
                            if values['vat'] != "XAXX010101000":
                                dup_ids = contact.env['res.partner'].search([('vat', '=', values['vat'])])
                                if dup_ids:
                                    raise Warning('RFC debe ser unico, este ya ha sido registrado!')
            
        contact = super(ResPartner, self).write(values)

        return contact
        

    #===================================Calcular limite restante=================================

    @api.depends('credit_limit')
    def _get_limit(self):
        invoices = self.env['account.invoice'].search(['&','&',('partner_id', '=', self.id),('type', '=', 'out_invoice'),('state', '=', 'open')])
        credit=self.credit_limit
        total=0
        
        for invoice in invoices:
            total+=invoice.amount_total
            credit-=invoice.amount_total
        
        self.limit_consumed=total
        self.limit_available=credit


    limit_consumed = fields.Float(string="Limit consumed", compute="_get_limit")
    limit_available = fields.Float(string="Limit available", compute="_get_limit")
        