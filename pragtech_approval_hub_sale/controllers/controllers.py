# -*- coding: utf-8 -*-
# from odoo import http


# class PragtechApprovalSale(http.Controller):
#     @http.route('/pragtech_approval_hub_sale/pragtech_approval_hub_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pragtech_approval_hub_sale/pragtech_approval_hub_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pragtech_approval_hub_sale.listing', {
#             'root': '/pragtech_approval_hub_sale/pragtech_approval_hub_sale',
#             'objects': http.request.env['pragtech_approval_hub_sale.pragtech_approval_hub_sale'].search([]),
#         })

#     @http.route('/pragtech_approval_hub_sale/pragtech_approval_hub_sale/objects/<model("pragtech_approval_hub_sale.pragtech_approval_hub_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pragtech_approval_hub_sale.object', {
#             'object': obj
#         })
