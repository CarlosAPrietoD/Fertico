from odoo import models, fields, api

class RecibaOrder(models.Model):
    _name = 'reciba.order'
    _description = 'Reciba'

    @api.one
    @api.depends('gross_weight', 'tare_weight')
    def _get_net(self):
        self.net_weight=self.gross_weight-self.tare_weight

    @api.one
    @api.depends('net_weight', 'discount_kilos_humidity')
    def _calculate_d_humidity(self):
        self.discount_humidity = (self.net_weight * self.discount_kilos_humidity) / 1000

    @api.one
    @api.depends('net_weight', 'discount_kilos_impurity')
    def _calculate_d_impurity(self):
        self.discount_impurity = (self.net_weight * self.discount_kilos_impurity) / 1000

    @api.one
    @api.depends('net_weight', 'discount_kilos_damaged')
    def _calculate_d_damaged(self):
        self.discount_damaged = (self.net_weight * self.discount_kilos_damaged) / 1000

    @api.one
    @api.depends('net_weight', 'discount_kilos_broken')
    def _calculate_d_broken(self):
        self.discount_broken = (self.net_weight * self.discount_kilos_broken) / 1000


    date = fields.Date(string="Date")
    customer_id = fields.Many2one('res.partner', string="Productor name")
    cycle_id = fields.Many2one('reciba.cycle', string="Cycle")
    #=======================Bascula====================
    no_ticket = fields.Char(string="No. ticket", required=True)
    third_folio = fields.Char(string="Third folio")
    reciba_third = fields.Char(string="Reciba for third customer")
    product_id = fields.Many2one('product.product', string="Product")
    modality_id = fields.Many2one('reciba.modality', string="Modality")
    silo = fields.Char(string='warehouse or silo')
    #======================Descuentos==================
    percentage_humidity = fields.Many2one('reciba.datatd', string="Humidity %", domain="['&',('product_id', '=', product_id),('condition', '=', 'humedad')]")
    discount_kilos_humidity = fields.Float(related='percentage_humidity.discount', string="Discount in kilos humidity", store=True)
    discount_humidity = fields.Float(string="Discount or humidity 14% to more", compute="_calculate_d_humidity", store=True, digits = (12,5))
    percentage_impurity = fields.Many2one('reciba.datatd', string="Impurity %", domain="['&',('product_id', '=', product_id),('condition', '=', 'impureza')]")
    discount_kilos_impurity = fields.Float(related='percentage_impurity.discount', string="Discount in kilos impurity", store=True)
    discount_impurity = fields.Float(string="Discount of impurity 2.5% to more", compute="_calculate_d_impurity", store=True, digits = (12,5))
    percentage_damaged = fields.Many2one('reciba.datatd', string="Damaged grain %", domain="['&',('product_id', '=', product_id),('condition', '=', 'danado')]")
    discount_kilos_damaged = fields.Float(related='percentage_damaged.discount', string="Discount in kilos damaged grain", store=True)
    discount_damaged = fields.Float(string="Discount of damaged grain", compute="_calculate_d_damaged", store=True, digits = (12,5))
    percentage_broken = fields.Many2one('reciba.datatd', string="Broken grain %", domain="['&',('product_id', '=', product_id),('condition', '=', 'quebrado')]")
    discount_kilos_broken = fields.Float(related='percentage_broken.discount', string="Discount in kilos broken grain", store=True)
    discount_broken = fields.Float(string="Discount of broken grain 5.5% to more", compute="_calculate_d_broken", store=True, digits = (12,5))
    sum_discounts = fields.Float(string="sum calculated discounts")
    discount_applied = fields.Float(string="Discount applied")

    free_qty = fields.Float(string="Free quantity")
    #========================Logistica================================
    operator = fields.Char(string="Operator name")
    plate = fields.Char(string="Placas")
    gross_weight = fields.Float(string="Gross weight")
    tare_weight = fields.Float(string="Tare weight")
    net_weight = fields.Float(string="Net weight", compute="_get_net", store=True)
    #========================Pago====================================
    net_weight_discount = fields.Float(string="Net weight to pay with discount")
    change_type = fields.Float(string="Change type")
    price_usd = fields.Char(string="Price agreed USD")
    unit_price = fields.Float(string="Unit price")
    currency = fields.Many2one('res.currency', string="Currency")
    amount_pay = fields.Float(string="Import to pay cheque")
    incentive = fields.Float(string="Incent.")
    freigh_threshing_discount = fields.Float("Freight and threshing discount")
    #=========================Programacion de pagos==================
    number_cheque = fields.Char("Cheque number")
    amount_cheque = fields.Float("Amount cheque")
    collection_date = fields.Date("Collection date")
    folio_bill = fields.Char("Folio Bill")
    payment_date = fields.Char("Payment date")
    observations = fields.Text("Observations")

    
    

    def name_get(self):
        res=[]
        for reciba in self:
            res.append((reciba.id,reciba.no_ticket))
        return res


