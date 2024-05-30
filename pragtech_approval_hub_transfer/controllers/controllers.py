# -*- coding: utf-8 -*-
# from odoo import http


# class PragtechApprovalHubTransfer(http.Controller):
#     @http.route('/pragtech_approval_hub_transfer/pragtech_approval_hub_transfer', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pragtech_approval_hub_transfer/pragtech_approval_hub_transfer/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pragtech_approval_hub_transfer.listing', {
#             'root': '/pragtech_approval_hub_transfer/pragtech_approval_hub_transfer',
#             'objects': http.request.env['pragtech_approval_hub_transfer.pragtech_approval_hub_transfer'].search([]),
#         })

#     @http.route('/pragtech_approval_hub_transfer/pragtech_approval_hub_transfer/objects/<model("pragtech_approval_hub_transfer.pragtech_approval_hub_transfer"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pragtech_approval_hub_transfer.object', {
#             'object': obj
#         })
