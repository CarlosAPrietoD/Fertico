from odoo import models, fields, api

class CreditPreApplication(models.Model):
    _name = "credit.preapplication"
    _inherit = ['mail.thread']

    @api.depends('crop_type_ids')
    def get_amount(self):
        amount = 0
        
        for line in self.crop_type_ids:
            amount += line.calculated_amount

        self.calculated_amount = amount

    def _get_name(self):
        count = self.env['credit.preapplication'].search([('company_id','=',self.env.user.company_id.id)])
        number = str(len(count)+1).zfill(4)
        return 'PRE-'+number


    state = fields.Selection([('draft', 'Borrador'),
    ('locked', 'Bloqueado')], default='draft')
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('credit.preapplication'))
    name = fields.Char('Preaplicación', default=_get_name, readonly=True)
    partner_id = fields.Many2one('res.partner', string="Cliente")
    cycle =  fields.Many2one('credit.cycles', string="Ciclo")
    crop_method = fields.Selection([('irrigation', 'Riego'),('rainwater', 'Temporal')], string="Metodo de cultivo")
    calculated_amount = fields.Float(string="Monto permitido", compute="get_amount", store=True)
    requested_amount = fields.Float(string="Monto solicitado")
    authorized_amount = fields.Float(string="Monto autorizado")
    insurance = fields.Float(string="Seguro Agrícola", compute="get_amount", store=True)
    credit_type_id = fields.Many2one('credit.types', string="Tipo de crédito")
    payment_terms = fields.Many2one(related='credit_type_id.payment_terms', string="Plazo de pago", readonly='True')
    date_limit_flag = fields.Boolean(default="False")
    date_limit = fields.Date(string="Fecha límite")
    interest = fields.Float(related='credit_type_id.interest', string="Interés", readonly='True')
    interest_mo = fields.Float(related='credit_type_id.interest_mo', string="Interés moratorio", readonly='True')
    crop_type_ids = fields.One2many('credit.crop.type', 'preapplication_id', string="Tipos de cultivo")

    @api.onchange('payment_terms')
    def get_payment_term(self):

        if self.payment_terms and len(self.payment_terms.line_ids) > 1:
            
            if self.payment_terms.line_ids[1].days == 180:
                self.date_limit_flag = True
            else:
                self.date_limit_flag = False
                self.date_limit = ''
        else:
            self.date_limit_flag = False
            self.date_limit = ''

    def lock_credit(self):

        self.state = 'locked'


class CreditCropType(models.Model):
    _name = "credit.crop.type"
    #Tipos de cultivo

    @api.one
    @api.depends('crop_type_id','crop_method','hectares')
    def get_amount(self):
        amount = 0
        
        if self.crop_type_id and self.crop_method:
            param = self.env['credit.parameters'].search([('crop_type','=',self.crop_type_id.id),('crop_method','=',self.crop_method)])
            if param:
                amount = param.amount*self.hectares

        self.calculated_amount = amount

    preapplication_id = fields.Many2one('credit.preapplication')
    crop_method = fields.Selection(related="preapplication_id.crop_method", string="Metodo de cultivo", readonly=True)
    crop_type_id = fields.Many2one('product.product', string="Tipo de cultivo")
    hectares = fields.Float(string="Hectareas")
    calculated_amount = fields.Float(string="Monto permitido", compute="get_amount", store=True)
    