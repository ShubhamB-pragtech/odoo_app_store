# -*- coding: utf-8 -*-
# from odoo import http


# class PragtechApprovalHubPayment(http.Controller):
#     @http.route('/pragtech_approval_hub_payment/pragtech_approval_hub_payment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pragtech_approval_hub_payment/pragtech_approval_hub_payment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pragtech_approval_hub_payment.listing', {
#             'root': '/pragtech_approval_hub_payment/pragtech_approval_hub_payment',
#             'objects': http.request.env['pragtech_approval_hub_payment.pragtech_approval_hub_payment'].search([]),
#         })

#     @http.route('/pragtech_approval_hub_payment/pragtech_approval_hub_payment/objects/<model("pragtech_approval_hub_payment.pragtech_approval_hub_payment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pragtech_approval_hub_payment.object', {
#             'object': obj
#         })
