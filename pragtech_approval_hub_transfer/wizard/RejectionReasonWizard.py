from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RejectionReasonWizard(models.TransientModel):
    _name = 'stock.reason.wizard'

    reason = fields.Text(string='Rejection Reason', required=True)
    stock_order_id = fields.Many2one('stock.picking', 'Stock Order', domain="[('state', '=', 'waiting_approval')]", ondelete='cascade')

    @api.model
    def default_get(self, fields_list):
        result = super(RejectionReasonWizard, self).default_get(fields_list)

        if self.env.context.get('active_model') == 'stock.picking' and self.env.context.get('active_id'):
            result['stock_order_id'] = self.env['stock.picking'].sudo().browse(self.env.context.get('active_id')).id

        return result

    def action_submit_rejection_reason(self):
        self.ensure_one()
        logged_in_user = self.env.user
        user_line = False

        if self.stock_order_id:
            user_line = self.env['approvehub.stock.user.line'].sudo().search([
                ('user_id', '=', logged_in_user.id),
                ('status', '=', 'waiting_approval'),
                ('stock_order_id', '=', self.stock_order_id.id)
            ], limit=1)

        if user_line:
            user_line.status = 'rejected'
            if self.stock_order_id:
                self.stock_order_id.state = 'rejected'
            user_line.rejection_reason = self.reason
            context = {'reason': self.reason}
            if self.stock_order_id:
                template = self.env.ref('pragtech_approval_hub_transfer.reject_inventory_stock_email_template')
                self.stock_order_id.write({'reason': self.reason})
                template.with_context(context).send_mail(self.stock_order_id.id,force_send=True)

            return {'type': 'ir.actions.act_window_close'}
        else:
            raise ValidationError(_("You don't have permission to reject this order."))
