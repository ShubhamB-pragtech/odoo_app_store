# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class pragtech_approval_hub(models.Model):
#     _name = 'pragtech_approval_hub.pragtech_approval_hub'
#     _description = 'pragtech_approval_hub.pragtech_approval_hub'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
