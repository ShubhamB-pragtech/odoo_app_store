# -*- coding: utf-8 -*-
# from odoo import http


# class PragtechApprovalBase(http.Controller):
#     @http.route('/pragtech_approval_hub/pragtech_approval_hub', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pragtech_approval_hub/pragtech_approval_hub/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pragtech_approval_hub.listing', {
#             'root': '/pragtech_approval_hub/pragtech_approval_hub',
#             'objects': http.request.env['pragtech_approval_hub.pragtech_approval_hub'].search([]),
#         })

#     @http.route('/pragtech_approval_hub/pragtech_approval_hub/objects/<model("pragtech_approval_hub.pragtech_approval_hub"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pragtech_approval_hub.object', {
#             'object': obj
#         })
