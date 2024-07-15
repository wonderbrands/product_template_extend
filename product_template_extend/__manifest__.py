# -*- coding: utf-8 -*-
{
    'name': 'Product Template Extend',
    'version': '1.0',
    'summary': 'Add fields to the product template',
    'description': 'This module allows you to add fields to the product template.',
    'author': '"Sergio Guerrero"',
    'depends': ['base',
                'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/product_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
