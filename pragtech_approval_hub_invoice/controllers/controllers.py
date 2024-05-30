# -*- coding: utf-8 -*-
# from odoo import http


# class ApporvalInvoice(http.Controller):
#     @http.route('/apporval_invoice/apporval_invoice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/apporval_invoice/apporval_invoice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('apporval_invoice.listing', {
#             'root': '/apporval_invoice/apporval_invoice',
#             'objects': http.request.env['apporval_invoice.apporval_invoice'].search([]),
#         })

#     @http.route('/apporval_invoice/apporval_invoice/objects/<model("apporval_invoice.apporval_invoice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('apporval_invoice.object', {
#             'object': obj
#         })
