from odoo import models, fields, api

class CreditPreApplication(models.Model):
    _name = "credit.preapplication"
    _inherit = ['mail.thread']
    #Pre-solicitudes


    @api.depends('crop_type_ids')
    def get_amount(self):
        amount = 0
        insurance = 0
        
        for line in self.crop_type_ids:
            amount += line.calculated_amount
            insurance += line.calculated_insurance

        self.calculated_amount = amount
        self.insurance = insurance

    def _get_name(self):
        count = self.env['credit.preapplication'].search([('company_id','=',self.env.user.company_id.id)])
        number = str(len(count)+1).zfill(4)
        return 'PRE-'+number


    #==============================================Campos generales de pre-aplicación=====================================
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('credit.preapplication'))
    state = fields.Selection([('draft', 'Borrador'),
    ('pre', 'Pre-solicitud'),
    ('committee','Comité de crédito'),
    ('credit','Crédito en curso'),
    ('rejected','Rechazado'),
    ('liquidated','Liquidado'),
    ('locked', 'Bloqueado')], default='draft')
    name = fields.Char('Preaplicación', default="Solicitud borrador", readonly=True)
    record_id = fields.Many2one('credit.record', string="Expediente")
    partner_id = fields.Many2one(related='record_id.partner_id', string="Solicitante")
    credit_type_id = fields.Many2one(related='record_id.credit_type_id', string="Tipo de crédito")
    cycle =  fields.Many2one('credit.cycles', string="Ciclo")
    payment_terms = fields.Many2one(related='credit_type_id.payment_terms', string="Plazo de pago", readonly='True')
    date_limit_flag = fields.Boolean(default="False")
    date_limit = fields.Date(string="Fecha límite")
    
    date = fields.Date(string="Fecha de solicitud")
    calculated_amount = fields.Float(string="Monto permitido total", compute="get_amount", store=True)
    requested_amount = fields.Float(string="Monto solicitado")
    investment_concept = fields.Char(string="Concepto de inversión")
    authorized_amount = fields.Float(string="Monto autorizado")
    insurance = fields.Float(string="Seguro Agrícola", compute="get_amount", store=True)
    interest = fields.Float(related='credit_type_id.interest', string="Interes", readonly='True')
    interest_mo = fields.Float(related='credit_type_id.interest_mo', string="Interes moratorio", readonly='True')
    
    #========================================== Datos de cultivo ===============================================
    crop_method = fields.Selection([('irrigation', 'Riego'),('rainwater', 'Temporal')], string="Metodo de cultivo")
    crop_type_ids = fields.One2many('credit.crop.type', 'preapplication_id', string="Tipos de cultivo")

    #========================================== Datos generales de contacto ===================================
    address = fields.Text(string="Dirección")
    suburb = fields.Char(string="Colonia")
    locality = fields.Char(string="Municipio/Localidad")
    state_address = fields.Char(string="Estado")
    postal_code = fields.Char(string="Código postal")
    phone_house = fields.Char(string="Teléfono (casa)")
    phone_personal = fields.Char(string="Teléfono (celular)")
    gender = fields.Selection([('m','Masculino'),('f','Femenino')], string="Género")
    email = fields.Char(string="E-mail")
    activity = fields.Char(string="Actividad económica")
    activity_second = fields.Char(string="Actividad económica secundaria")
    identification = fields.Selection([('ine','IFE/INE'),('pass','Pasaporte')], string="Identificación")
    identification_number = fields.Char(string="No. de identificación")
    civil_status = fields.Selection([('single', 'Soltero'),
    ('married','Casado'),
    ('property', 'Regimen separación bienes'),
    ('society','Sociedad conyugal'),
    ('widower', 'Viudo'),
    ('free', 'Union libre')], string="Estado civil")
    rfc = fields.Char(string="RFC")
    curp = fields.Char(string="CURP")



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

    @api.multi
    def open_report_buro(self):
        return {
                'name': 'Cash Control',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'credit.application.buro',
                'view_id': self.env.ref('wobin_credit.report_data_application_buro').id,
                'type': 'ir.actions.act_window',
                'res_id': self.env.context.get('cashbox_id'),
                'context': {'default_application_id':self.id},
                'target': 'new'
            }


class CreditCropType(models.Model):
    _name = "credit.crop.type"
    #Tipos de cultivo

    @api.one
    @api.depends('crop_type_id','crop_method','hectares')
    def get_amount(self):
        amount = 0
        insurance = 0
        
        if self.crop_type_id and self.crop_method:
            param = self.env['credit.parameters'].search([('crop_type','=',self.crop_type_id.id),('crop_method','=',self.crop_method)])
            if param:
                amount = param.amount*self.hectares
                insurance = param.insurance*self.hectares

        self.calculated_amount = amount
        self.calculated_insurance = insurance

    preapplication_id = fields.Many2one('credit.preapplication')
    crop_method = fields.Selection(related="preapplication_id.crop_method", string="Metodo de cultivo", readonly=True)
    crop_type_id = fields.Many2one('product.product', string="Tipo de cultivo")
    hectares = fields.Float(string="Hectareas")
    calculated_amount = fields.Float(string="Monto permitido", compute="get_amount", store=True)
    calculated_insurance = fields.Float(string="Seguro agrícola", compute="get_amount", store=True)