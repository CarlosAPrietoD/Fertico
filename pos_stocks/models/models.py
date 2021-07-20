# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd.
#    (<https://webkul.com/>)
#
###############################################################################
import logging
import psycopg2

from odoo import api, fields, models, tools
_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _get_group_pos_allow_payment(self):
        return self.env.ref('pos_stocks.allow_create_payment', False)

    wk_display_stock = fields.Boolean('Display stock in POS', default=True)

    wk_stock_type = fields.Selection(
        (
            ('available_qty', 'Available Quantity(On hand)'),
            ('forecasted_qty', 'Forecasted Quantity'),
            ('virtual_qty', 'Quantity on Hand - Outgoing Qty')
        ), string='Stock Type', default='available_qty')
    wk_continous_sale = fields.Boolean('Allow Order When Out-of-Stock')
    wk_deny_val = fields.Integer('Deny order when product stock is'
                                 ' lower than ')
    wk_error_msg = fields.Char(string='Custom message',
                               default="Product out of stock")
    wk_hide_out_of_stock = fields.Boolean(string="Hide Out of Stock products",
                                          default=True)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        required=True, readonly=True, default=_default_currency,
        track_visibility='always')

    def refund(self):
        res = super(PosOrder, self.with_context(use_session=True)).refund()
        return res

    def action_pos_order_paid(self):
        try:
            return super(PosOrder, self).action_pos_order_paid()
        except psycopg2.OperationalError:
            # do not hide transactional errors, the order(s) won't be saved!
            raise
        except BaseException as e:
            _logger.error(
                'Could not fully process the POS Order: %s', tools.ustr(e))

    @api.model
    def get_details(self, ref):
        order_id = self.env['pos.order'].sudo().search([
            ('pos_reference', '=', ref)], limit=1)
        return order_id.ids

    @api.model
    def get_orderlines(self, ref):
        discount = 0
        result = []
        order_id = self.search([('pos_reference', '=', ref)], limit=1)
        lines = self.env['pos.order.line'].search([
            ('order_id', '=', order_id.id)])
        payments = self.env['account.bank.statement.line'].search([
            ('pos_statement_id', '=', order_id.id)])
        payment_lines = []
        change = 0
        for i in payments:
            if i.amount > 0:
                temp = {
                    'amount': i.amount,
                    'name': i.journal_id.name
                }
                payment_lines.append(temp)
            else:
                change += i.amount
        for line in lines:
            new_vals = {
                'product_id': line.product_id.name,
                'qty': line.qty,
                'price_unit': line.price_unit,
                'discount': line.discount,
                }
            discount += (line.price_unit * line.qty * line.discount) / 100
            result.append(new_vals)

        return [result, discount, payment_lines, change]
