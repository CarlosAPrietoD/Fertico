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
        

#=========================================Unificar contactos================================================
class ContactWizard(models.TransientModel):
    _name = "contact.wizard"
    #En un wizard pedimos el contacto que se va a eliminar
    contact=fields.Many2one('res.partner', string="Contact to delete")

    def unify_contact(self):
        #recuperamos los 2 contactos con los que vamos a trabajar
        contact_main = self.env['res.partner'].browse(self._context.get('active_ids'))[0]
        contact_delete = self.contact.id

        #hacemos una busqueda con todos los modelos que tengan relacion con el contacto que se va a eliminar
        #se hace el cambio de registros del contacto que se eliminará al contacto que se va a conservar
        accounts = self.env['account.analytic.account'].search([('partner_id','=',contact_delete)])
        for account in accounts:
            account.partner_id=contact_main
        analytics = self.env['account.analytic.line'].search([('partner_id','=',contact_delete)])
        for analytic in analytics:
            analytic.partner_id=contact_main
        banks = self.env['account.bank.statement.line'].search([('partner_id','=',contact_delete)])
        for bank in banks:
            bank.partner_id=contact_main
        invoices = self.env['account.invoice'].search([('partner_id','=',contact_delete)])
        for invoice in invoices:
            invoice.partner_id = contact_main
        invoices = self.env['account.invoice'].search([('commercial_partner_id','=',contact_delete)])
        for invoice in invoices:
            invoice.commercial_partner_id = contact_main
        invoices = self.env['account.invoice'].search([('partner_shipping_id','=',contact_delete)])
        for invoice in invoices:
            invoice.partner_shipping_id = contact_main
        invoice_lines = self.env['account.invoice.line'].search([('partner_id','=',contact_delete)])
        for line in invoice_lines:
            line.partner_id=contact_main
        invoice_reports = self.env['account.invoice.report'].search([('partner_id','=',contact_delete)])
        for report in invoice_reports:
            report.partner_id=contact_main
        invoice_reports = self.env['account.invoice.report'].search([('commercial_partner_id','=',contact_delete)])
        for report in invoice_reports:
            report.commercial_partner_id=contact_main
        moves = self.env['account.move'].search([('partner_id','=',contact_delete)])
        for move in moves:
            move.partner_id=contact_main
        move_lines = self.env['account.move.line'].search([('partner_id','=',contact_delete)])
        for line in move_lines:
            line.partner_id = contact_main
        payments = self.env['account.payment'].search([('partner_id','=',contact_delete)])
        for payment in payments:
            payment.partner_id=contact_main
        payments = self.env['account.register.payments'].search([('partner_id','=',contact_delete)])
        for payment in payments:
            payment.partner_id=contact_main
        managers = self.env['account.report.manager'].search([('partner_id','=',contact_delete)])
        for manager in managers:
            manager.partner_id=contact_main
        bases = self.env['base.automation.lead.test'].search([('partner_id','=',contact_delete)])
        for base in bases:
            base.partner_id=contact_main
        employees = self.env['hr.employee'].search([('address_id','=',contact_delete)])
        for employee in employees:
            employee.address_id=contact_main
        employees = self.env['hr.employee'].search([('address_home_id','=',contact_delete)])
        for employee in employees:
            employee.address_home_id=contact_main
        mails = self.env['mail.channel.partner'].search([('partner_id','=',contact_delete)])
        for mail in mails:
            mail.partner_id=contact_main
        msgs = self.env['mail.compose.message'].search([('author_id','=',contact_delete)])
        for msg in msgs:
            msg.author_id=contact_main
        followers = self.env['mail.followers'].search([('partner_id','=',contact_delete)])
        for follower in followers:
            follower.partner_id=contact_main
        mails = self.env['mail.mail'].search([('author_id','=',contact_delete)])
        for mail in mails:
            mail.author_id=contact_main
        msgs = self.env['mail.message'].search([('author_id','=',contact_delete)])
        for msg in msgs:
            msg.author_id=contact_main
        notifications = self.env['mail.notification'].search([('res_partner_id','=',contact_delete)])
        for notification in notifications:
            notification.res_partner_id=contact_main
        devices = self.env['mail_push.device'].search([('partner_id','=',contact_delete)])
        for device in devices:
            device.partner_id=contact_main
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
        infos = self.env['product.supplierinfo'].search([('name','=',contact_delete)])
        for info in infos:
            info.name=contact_main
        purchases = self.env['purchase.order'].search([('partner_id','=',contact_delete)])
        for purchase in purchases:
            purchase.partner_id = contact_main
        purchases = self.env['purchase.order'].search([('dest_address_id','=',contact_delete)])
        for purchase in purchases:
            purchase.dest_address_id=contact_main
        purchases = self.env['purchase.order.line'].search([('partner_id','=',contact_delete)])
        for purchase in purchases:
            purchase.partner_id=contact_main
        reports = self.env['purchase.report'].search([('partner_id','=',contact_delete)])
        for report in reports:
            report.partner_id=contact_main
        reports = self.env['purchase.report'].search([('commercial_partner_id','=',contact_delete)])
        for report in reports:
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
        users = self.env['res.users'].search([('commercial_partner_id','=',contact_delete)])
        for user in users:
            user.commercial_partner_id=contact_main
        users = self.env['res.users'].search([('parent_id','=',contact_delete)])
        for user in users:
            user.parent_id=contact_main
        users = self.env['res.users'].search([('partner_id','=',contact_delete)])
        for user in users:
            user.partner_id=contact_main
        users = self.env['res.users'].search([('self','=',contact_delete)])
        for user in users:
            user.self=contact_main
        orders = self.env['sale.order'].search([('partner_id','=',contact_delete)])
        for order in orders:
            order.partner_id=contact_main
        orders = self.env['sale.order'].search([('partner_invoice_id','=',contact_delete)])
        for order in orders:
            order.partner_invoice_id=contact_main
        orders = self.env['sale.order'].search([('partner_shipping_id','=',contact_delete)])
        for order in orders:
            order.partner_shipping_id=contact_main
        order_lines = self.env['sale.order.line'].search([('order_partner_id','=',contact_delete)])
        for line in order_lines:
            line.order_partner_id=contact_main
        reports = self.env['sale.report'].search([('partner_id','=',contact_delete)])
        for report in reports:
            report.partner_id=contact_main
        reports = self.env['sale.report'].search([('commercial_partner_id','=',contact_delete)])
        for report in reports:
            report.commercial_partner_id=contact_main
        inventorys = self.env['stock.inventory'].search([('partner_id','=',contact_delete)])
        for inventory in inventorys:
            inventory.partner_id=contact_main
        lines = self.env['stock.inventory.line'].search([('partner_id','=',contact_delete)])
        for line in lines:
            line.partner_id=contact_main
        locations = self.env['stock.location'].search([('partner_id','=',contact_delete)])
        for location in locations:
            location.partner_id=contact_main
        moves = self.env['stock.move'].search([('partner_id','=',contact_delete)])
        for move in moves:
            move.partner_id=contact_main
        moves = self.env['stock.move'].search([('picking_partner_id','=',contact_delete)])
        for move in moves:
            move.picking_partner_id=contact_main
        moves = self.env['stock.move'].search([('restrict_partner_id','=',contact_delete)])
        for move in moves:
            move.restrict_partner_id=contact_main
        move_lines = self.env['stock.move.line'].search([('owner_id','=',contact_delete)])
        for line in move_lines:
            line.owner_id=contact_main
        pickings = self.env['stock.picking'].search([('partner_id','=',contact_delete)])
        for picking in pickings:
            picking.partner_id=contact_main
        pickings = self.env['stock.picking'].search([('owner_id','=',contact_delete)])
        for picking in pickings:
            picking.owner_id=contact_main
        quants = self.env['stock.quant'].search([('owner_id','=',contact_delete)])
        for quant in quants:
            quant.owner_id=contact_main
        packages = self.env['stock.quant.package'].search([('owner_id','=',contact_delete)])
        for package in packages:
            package.owner_id=contact_main
        scraps = self.env['stock.scrap'].search([('owner_id','=',contact_delete)])
        for scrap in scraps:
            scrap.owner_id=contact_main
        warehouses = self.env['stock.warehouse'].search([('partner_id','=',contact_delete)])
        for warehouse in warehouses:
            warehouse.partner_id

        #Eliminamos el contacto
        self.contact.unlink()
#===============================fin unificar contactos================================================