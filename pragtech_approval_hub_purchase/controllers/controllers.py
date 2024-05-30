# -*- coding: utf-8 -*-
# from odoo import http


# class PragtechApprovalPurchase(http.Controller):
#     @http.route('/pragtech_approval_hub_purchase/pragtech_approval_hub_purchase', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pragtech_approval_hub_purchase/pragtech_approval_hub_purchase/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pragtech_approval_hub_purchase.listing', {
#             'root': '/pragtech_approval_hub_purchase/pragtech_approval_hub_purchase',
#             'objects': http.request.env['pragtech_approval_hub_purchase.pragtech_approval_hub_purchase'].search([]),
#         })

#     @http.route('/pragtech_approval_hub_purchase/pragtech_approval_hub_purchase/objects/<model("pragtech_approval_hub_purchase.pragtech_approval_hub_purchase"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pragtech_approval_hub_purchase.object', {
#             'object': obj
#         })
