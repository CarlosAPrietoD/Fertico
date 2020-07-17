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
        contact_main = self.env['res.partner'].browse(self._context.get('active_ids'))[0]
        contact_delete = self.contact.id

        
        sales = self.env['sale.order'].search([('partner_id','=',contact_delete)])
        payments = self.env['account.abstract.payment'].search([('partner_id','=',contact_delete)])
        for payment in payments:
            payment.partner_id=contact_main
        accounts = self.env['account.analytic.account'].search([('partner_id','=',contact_delete)])
        for account in accounts:
            account.partner_id=contact_main
            if account.message_partner_ids:
                account.message_partner_ids=contact_main
        analytics = self.env['account.analytic.line'].search([('partner_id','=',contact_delete)])
        for analytic in analytics:
            analytic.partner_id=contact_main
        banks = self.env['account.bank.statement'].search([('message_partner_ids','=',contact_delete)])
        for bank in banks:
            bank.message_partner_ids=contact_main
        banks = self.env['account.bank.statement.line'].search([('partner_id','=',contact_delete)])
        for bank in banks:
            bank.partner_id=contact_main
        invoices = self.env['account.invoice'].search([('partner_id','=',contact_delete)])
        for invoice in invoices:
            invoice.partner_id = contact_main
            invoice.commercial_partner_id = contact_main
            invoice.message_partner_ids = contact_main
            invoice.partner_shipping_id = contact_main
        invoice_lines = self.env['account.invoice.line'].search([('partner_id','=',contact_delete)])
        for line in invoice_lines:
            line.partner_id=contact_main
        invoice_reports = self.env['account.invoice.report'].search([('partner_id','=',contact_delete)])
        for report in invoice_reports:
            report.partner_id=contact_main
            report.commercial_partner_id=contact_main
        moves = self.env['account.move'].search([('partner_id','=',contact_delete)])
        for move in moves:
            move.partner_id=contact_main
        move_lines = self.env['account.move.line'].search([('partner_id','=',contact_delete)])
        for line in move_lines:
            line.partner_id = contact_main
        providers = self.env['account.online.provider'].search([('message_partner_ids','=',contact_delete)])
        for provider in providers:
            provider.message_partner_ids=contact_main
        payments = self.env['account.payment'].search([('partner_id','=',contact_delete)])
        for payment in payments:
            payment.partner_id=contact_main
            payment.message_partner_ids=contact_main
        payments = self.env['account.register.payments'].search([('partner_id','=',contact_delete)])
        for payment in payments:
            payment.partner_id=contact_main
        managers = self.env['account.report.manager'].search([('partner_id','=',contact_delete)])
        for manager in managers:
            manager.partner_id=contact_main
        bases = self.env['base.automation.lead.test'].search([('partner_id','=',contact_delete)])
        for base in bases:
            base.partner_id=contact_main
        teams = self.env['crm.team'].search([('message_partner_ids','=',contact_delete)])
        for team in teams:
            team.message_partner_ids=[(6,0,[contact_main])]
        emails = self.env['email_template.preview'].search([('partner_ids','=',contact_delete)])
        for email in emails:
            email.partner_ids=contact_main
        departaments = self.env['hr.department'].search([('message_partner_ids','=',contact_delete)])
        for departament in departaments:
            departament.message_partner_ids=contact_main
        employees = self.env['hr.employee'].search([('address_id','=',contact_delete)])
        for employee in employees:
            employee.address_id=contact_main
            employee.address_home_id=contact_main
            employee.message_partner_ids=contact_main
        jobs = self.env['hr.job'].search([('message_partner_ids','=',contact_delete)])
        for job in jobs:
            job.message_partner_ids=contact_main
        channels = self.env['mail.channel'].search([('channel_partner_ids','=',contact_delete)])
        for channel in channels:
            channel.channel_partner_ids=contact_main
            channel.message_partner_ids=contact_main
        mails = self.env['mail.channel.partner'].search([('partner_id','=',contact_delete)])
        for mail in mails:
            mail.partner_id=contact_main
        msgs = self.env['mail.compose.message'].search([('author_id','=',contact_delete)])
        for msg in msgs:
            msg.author_id=contact_main
            msg.needaction_partner_ids=contact_main
            msg.partner_ids=contact_main
            msg.starred_partner_ids=contact_main
        followers = self.env['mail.followers'].search([('partner_id','=',contact_delete)])
        for follower in followers:
            follower.partner_id=contact_main
        mails = self.env['mail.mail'].search([('author_id','=',contact_delete)])
        for mail in mail:
            mail.author_id=contact_main
            mail.needaction_partner_ids=contact_main
            mail.partner_ids=contact_main
            mail.recipient_ids=contact_main
            mail.starred_partner_ids=contact_main
        msgs = self.env['mail.message'].search([('author_id','=',contact_delete)])
        for msg in msgs:
            msg.author_id=contact_main
            msg.needaction_partner_ids=contact_main
            msg.partner_ids=contact_main
            msg.starred_partner_ids=contact_main
        notifications = self.env['mail.notification'].search([('res_partner_id','=',contact_delete)])
        for notification in notifications:
            notification.res_partner_id=contact_main
        devices = self.env['mail_push.device'].search([('partner_id','=',contact_delete)])
        for device in devices:
            device.partner_id=contact_main
        msgs = self.env['mail.test'].search([('message_partner_ids','=',contact_delete)])
        for msg in msgs:
            msg.message_partner_ids=contact_main
        tests = self.env['mail.test.simple'].search([('message_partner_ids','=',contact_delete)])
        for test in tests:
            test.message_partner_ids=contact_main
        msgs = self.env['mail.thread'].search([('message_partner_ids','=',contact_delete)])
        for msg in msgs:
            msg.message_partner_ids=contact_main
        tokens = self.env['payment.token'].search([('partner_id','=',contact_delete)])
        for token in tokens:
            token.partner_id=contact_main
        transactions = self.env['payment.transaction'].search([('partner_id','=',contact_delete)])
        for transaction in transactions:
            transaction.partner_id=contact_main
        orders = self.env['pos.order'].search([('partner_id','=',contact_delete)])
        for order in orders:
            order.partner_id=contact_main
        groups = self.env['procurement.group'].search([('partner_id','=',contact_delete)])
        for group in groups:
            group.partner_id=contact_main
        rules = self.env['procurement.rule'].search([('partner_address_id','=',contact_delete)])
        for rule in rules:
            rule.partner_address_id
        products = self.env['product.product'].search([('message_partner_ids','=',contact_delete)])
        for product in products:
            product.message_partner_ids=contact_main
        infos = self.env['product.supplierinfo'].search([('name','=',contact_delete)])
        for info in infos:
            info.name=contact_main
        templates = self.env['product.template'].search([('message_partner_ids','=',contact_delete)])
        for template in templates:
            template.message_partner_ids=contact_main
        purchases = self.env['purchase.order'].search([('partner_id','=',contact_delete)])
        for purchase in purchases:
            purchase.partner_id = contact_main
            purchase.dest_address_id=contact_main
            purchase.message_partner_ids=contact_main
        purchases = self.env['purchase.order.line'].search([('partner_id','=',contact_delete)])
        for purchase in purchases:
            purchase.partner_id=contact_main
        reports = self.env['purchase.report'].search([('partner_id','=',contact_delete)])
        for report in reports:
            report.partner_id=contact_main
            report.commercial_partner_id=contact_main
        companys = self.env['res.company'].search([('partner_id','=',contact_delete)])
        for company in companys:
            company.partner_id=contact_main
        partners = self.env['res.partner'].search([('parent_id','=',contact_delete)])
        for partner in partners:
            partner.parent_id=contact_main
        banks = self.env['res.partner.bank'].search([('partner_id','=',contact_delete)])
        for bank in banks:
            bank.partner_id=contact_main
        categorys = self.env['res.partner.category'].search([('partner_ids','=',contact_delete)])
        for category in categorys:
            category.partner_ids=contact_main
        users = self.env['res.users'].search([('partner_ids','=',contact_delete)])
        for user in users:
            user.child_ids=contact_main
            user.commercial_partner_id=contact_main
            user.message_partner_ids=contact_main
            user.parent_id=contact_main
            user.partner_id=contact_main
            user.self=contact_main
        orders = self.env['sale.order'].search([('partner_id','=',contact_delete)])
        for order in orders:
            order.partner_id=contact_main
            order.message_partner_ids=contact_main
            order.partner_invoice_id=contact_main
            order.partner_shipping_id
        



        
        for sale in sales:
            sale.partner_id = contact_main
            if sale.partner_invoice_id:
                sale.partner_invoice_id = contact_main
            if sale.partner_shipping_id:
                sale.partner_shipping_id = contact_main
        

        self.contact.unlink()