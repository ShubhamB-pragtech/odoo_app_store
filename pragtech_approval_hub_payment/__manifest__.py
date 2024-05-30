# -*- coding: utf-8 -*-
{
    'name': "Pragmatic Approve Hub Payment",
    'version': '16.0.4',
    'category': 'Services',
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'website': 'http://pragtech.co.in',
    'summary': 'Pragmatic Approve Hub Payment',
    'description': 'Pragmatic Approve Hub Payment',
    'depends': ['base','mail','pragtech_approval_hub','account'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/account_payment_view.xml',
        'data/approve_payment_template.xml',
        'data/submit_payment_template.xml',
        'data/reject_payment_template.xml',
        'wizard/RejectionReasonWizard.xml',

    ],
    'demo': ['demo/demo.xml'],
    'images': ['static/description/pragtech_approval_hub_payment_animated_banner.gif'],
    'live_test_url': 'http://www.pragtech.co.in/company/proposal-form.html?id=103&name=Pragmatic-Approve-Hub',
    'currency': 'USD',
    'price': 79,
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'auto_install': False,
}
