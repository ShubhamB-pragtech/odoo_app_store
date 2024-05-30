from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

class Picking(models.Model):
    _inherit = "stock.picking"
    _description = "Inventory"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waitingfor', 'Waiting For Approval'),
        ('approved', 'Approved'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('submit', 'Submitted'),
        ('rejected', 'Rejected'),
    ],
        string="Status", default='draft', copy=False, readonly=True)

    approval_user_line_ids = fields.One2many('approvehub.stock.user.line', 'stock_order_id', string='Users Line')
    is_configured = fields.Boolean(string="Is Configured", default=False)
    reason = fields.Text(string='Sale Order')
    is_visible_buttons = fields.Boolean(compute='_compute_is_visible_buttons_from_inventory_stock', readonly=False,
                                        store=False)

    def _compute_is_visible_buttons_from_inventory_stock(self):
        for order in self:
            approvehub_form = self.env['approvehub.form'].sudo().search([('model_id.model', '=', 'stock.picking')],
                                                                        limit=1)
            active_user_id = self.env.user.id
            user_ids = order.approval_user_line_ids.user_id.ids
            if active_user_id not in user_ids:
                order.is_visible_buttons = False
            else:
                for user_line in order.approval_user_line_ids:
                    if user_line.user_id.id == active_user_id:
                        if user_line.status == 'approved':
                            order.is_visible_buttons = False
                            return
                        elif user_line.state == 'mandatory':
                            if approvehub_form.domain_filter:
                                model_name = approvehub_form.model_id.model
                                domain = eval(approvehub_form.domain_filter)
                                if self.env[model_name].search_count(expression.AND([domain, [('id', '=', order.id)]])):
                                    order.is_visible_buttons = True
                                    return
                            else:
                                order.is_visible_buttons = True
                                return
                order.is_visible_buttons = False

    @api.model
    def default_get(self, fields_list):
        result = super(Picking, self).default_get(fields_list)
        approval_id = self.env['approvehub.form'].sudo().search([('model_id.model', '=', 'stock.picking')], limit=1)
        approval_line_list = []
        if approval_id:
            if approval_id.user_ids:
                for user_line in approval_id.user_ids:
                    if user_line.status == 'mandatory':
                        user_line_values = {
                            'user_id': user_line.user_id.id,
                            'status': 'waiting_approval',
                            'state': user_line.status,
                            'rejection_reason': ' ',
                        }
                        approval_user_line_id = self.env['approvehub.stock.user.line'].sudo().create(user_line_values)
                        approval_line_list.append(approval_user_line_id.id)

        result['approval_user_line_ids'] = [(6, 0, approval_line_list)]
        if approval_id and approval_id.state == 'submitted':
            result['is_configured'] = bool(approval_id)
        else:
            result['is_configured'] = False
        return result

    def action_submit(self):
        for order in self:
            approvehub_form = self.env['approvehub.form'].sudo().search([('model_id.model', '=', 'stock.picking')],
                                                                        limit=1)

            if approvehub_form.domain_filter:
                model_name = approvehub_form.model_id.model
                domain = eval(approvehub_form.domain_filter)
                if not self.env[model_name].search(expression.AND([domain, [('id', '=', order.id)]])):
                    order.state = 'draft'
                    order.is_configured = False
                    order.is_visible_buttons = False
                    return
                else:
                    order.state = 'waitingfor'
                    email_template = self.env.ref(
                        'pragtech_approval_hub_transfer.approval_submit_stock_order_template_id')
                    user_ids = order.approval_user_line_ids.mapped('user_id')
                    for user in user_ids:
                        email_values = {
                            'email_to': user.partner_id.email,
                        }
                        email_template.with_context(customer_name=user.name).send_mail(order.id, force_send=True,
                                                                                       email_values=email_values)
            else:
                order.state = 'waitingfor'
                email_template = self.env.ref(
                    'pragtech_approval_hub_transfer.approval_submit_stock_order_template_id')
                user_ids = order.approval_user_line_ids.mapped('user_id')
                for user in user_ids:
                    email_values = {
                        'email_to': user.partner_id.email,
                    }
                    email_template.with_context(customer_name=user.name).send_mail(order.id, force_send=True,
                                                                                   email_values=email_values)
    def action_approve(self):
        template_id = self.env.ref('pragtech_approval_hub_transfer.approval_approve_inventory_stock_template_id')
        for order in self:
            logged_in_user = self.env.user
            mandatory_user_lines = order.approval_user_line_ids.filtered(
                lambda line: line.state == 'mandatory' and line.status == 'waiting_approval'
            )
            if logged_in_user in mandatory_user_lines.mapped('user_id'):
                user_line = mandatory_user_lines.filtered(lambda line: line.user_id == logged_in_user)
                if user_line:
                    user_line.status = 'approved'
                    user_line.has_approved = True

                count = 0
                for user_line in order.approval_user_line_ids:
                    if user_line.status == 'approved':
                        count = count + 1

                approval_form = self.env['approvehub.form'].sudo().search([('model_id.model', '=', 'stock.picking')],
                                                                          limit=1)
                minimum_approvers = approval_form.minimum_users if approval_form else 0
                print("-------------------------------------------------------------------------", minimum_approvers)
                if minimum_approvers == 0:
                    if all(line.status == 'approved' for line in mandatory_user_lines):
                        order.state = 'approved'
                        order.is_configured = False
                        template_id.send_mail(order.id, force_send=True)

                elif count >= minimum_approvers:
                    order.state = 'approved'
                    order.is_configured = False
                    template_id.send_mail(order.id, force_send=True)
                else:
                    return True
            else:
                raise ValidationError(_("You don't have permission to Approve this order."))

    def action_reject(self):
        for order in self:
            logged_in_user = self.env.user
            user_line = order.approval_user_line_ids.filtered(
                lambda line: line.user_id == logged_in_user and line.status == 'waiting_approval'
            )
            if user_line:
                if user_line.state == 'mandatory':
                    return {
                        'name': _('Rejection Reason'),
                        'type': 'ir.actions.act_window',
                        'res_model': 'stock.reason.wizard',
                        'view_mode': 'form',
                        'target': 'new',
                    }
                else:
                    raise ValidationError(_("You don't have permission to Reject this order."))
            else:
                raise ValidationError(_("You don't have permission to reject this order."))


class ApprovalUserLine(models.Model):
    _name = 'approvehub.stock.user.line'

    user_id = fields.Many2one('res.users', string='User', required=True, readonly=True)
    status = fields.Selection([
        ('waiting_approval', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', required=True, default='waiting_approval', readonly=True)
    state = fields.Selection([
        ('mandatory', 'Mandatory'),
        ('not_mandatory', 'Not Mandatory'),
    ], string='Status', default='mandatory', readonly=True)
    stock_order_id = fields.Many2one('stock.picking', string="Inventory Stock", readonly=True)
    has_approved = fields.Boolean(string='Has Approved', default=False, readonly=True)
    has_rejected = fields.Boolean(string='Has Rejected', default=False, readonly=True)
    rejection_reason = fields.Text(string='Rejection Reason', readonly=True)

class ApproveHubForm(models.Model):
    _inherit = 'approvehub.form'

    @api.model
    def _get_account_domain(self):
        domain = expression.OR([
            super(ApproveHubForm, self)._get_account_domain(),
            [('model', '=', 'stock.picking')]
        ])
        return domain

    model_id = fields.Many2one(
        'ir.model',
        string='Model Name',
        domain=_get_account_domain
    )
