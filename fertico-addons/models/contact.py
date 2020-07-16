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
            if self.parent_id:
                if values.get('vat'):
                    parent_vat= self.env['res.partner'].search([('id', '=', self.parent_id.id)]).vat
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
            
        contact = super(ResPartner, self).write(values)

        return contact
        
#==============================Unificar contactos==================================

class ContactWizard(models.TransientModel):
    _name = "contact.wizard"

    contact=fields.Many2one('res.partner', string="Contact to unify")

    def unify_contact(self):
        active_id = self._context('active_ids')
        
        print("===========actual",active_id)
        print("==============a unificar",self.contact)