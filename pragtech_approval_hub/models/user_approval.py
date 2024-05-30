from odoo import models, fields

class ResUsersInherited(models.Model):
    _inherit = 'res.users'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    approvehub_form_id = fields.Many2one('approvehub.form', string='ApproveHub Form')
