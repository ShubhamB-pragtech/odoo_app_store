from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ApproveHubForm(models.Model):
    _name = 'approvehub.form'
    _description = 'Approval Form'

    shared_model_list = []
    def _get_account_domain(self):
        domain = [('model', 'in', self.shared_model_list)]
        return domain

    name = fields.Char(string='Reference', required=True)
    model_id = fields.Many2one('ir.model', string='Model',domain=_get_account_domain)
    user_ids = fields.One2many('approvehub.form.user.line', 'approvehub_form_id', string='Approvers', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
    ], string='State', default='draft', readonly=True, states={'draft': [('readonly', False)]})

    model_name = fields.Char(string='Model Name', related='model_id.model', readonly=True)
    domain_filter = fields.Text(string="Domain filter")
    mail_notification = fields.Boolean(string='Mail Notification')
    email_template_id = fields.Many2one('mail.template', string='Email Template',
                                        domain="[('model_id.model', '=', 'approvehub.form')]")
    minimum_users = fields.Integer(string='Minimum Approvers', default=0)


    @api.onchange('user_ids')
    def _check_unique_users(self):
        for order in self:
            order.state = 'draft'
        user_ids = self.mapped('user_ids.user_id')
        if len(user_ids) != len(set(user_ids)):
            raise ValidationError("Duplicate users selected in Approvers")

    def _check_mandatory_users(self):
        for form in self:
            mandatory_users = form.user_ids.filtered(lambda user: user.status == 'mandatory')
            if not mandatory_users:
                raise ValidationError("At least one user must have a mandatory status.")

    def action_submit_user(self):
        self._check_mandatory_users()
        for record in self:
            user_ids = record.user_ids.mapped('user_id')
            if not user_ids:
                raise ValidationError("At least one user must be added as an approver.")

            if record.mail_notification:
                emails = [user.partner_id.email for user in user_ids if user.partner_id.email]
                email_values = {'email_to': ','.join(emails)}

                if record.email_template_id:
                    record.email_template_id.send_mail(record.id, force_send=True, email_values=email_values)
                else:
                    raise ValidationError("Please select an email template.")
            else:
                default_template_id = self.env.ref('pragtech_approval_hub.approval_user_email_template_id')
                if not default_template_id:
                    raise ValidationError("Default email template is not found. Please configure it.")

                emails = [user.partner_id.email for user in user_ids if user.partner_id.email]
                email_values = {'email_to': ','.join(emails)}
                default_template_id.send_mail(record.id, force_send=True, email_values=email_values)

            record.state = 'submitted'

    def action_reset_draft(self):
        for order in self:
            order.state = 'draft'

    def unlink(self):
        for record in self:
            if record.state == 'submitted':
                raise ValidationError("You cannot delete a record in the Submitted state. Reset it to Draft first.")
        return super(ApproveHubForm, self).unlink()

    _sql_constraints = [
        ('unique_model_list', 'unique(model_id)',
         'An approval form for this model already exists.'),
    ]

class ApproveHubFormUserLine(models.Model):
    _name = 'approvehub.form.user.line'
    _description = 'Approval Form User Line'

    user_id = fields.Many2one('res.users', string='User')
    status = fields.Selection([
        ('mandatory', 'Mandatory'),
        ('not_mandatory', 'Not Mandatory'),
    ], string='Type of Approval', default='mandatory')

    approvehub_form_id = fields.Many2one('approvehub.form', string='Approval Form')

    _sql_constraints = [
        ('unique_user_in_approver', 'unique(user_id, approvehub_form_id)',
         'User cannot be added multiple times to the same form.'),
    ]